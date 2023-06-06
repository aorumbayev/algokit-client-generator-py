import dataclasses
import typing
from collections.abc import Iterable
from typing import Literal

import algokit_utils

from algokit_client_generator import utils
from algokit_client_generator.document import DocumentParts, Part
from algokit_client_generator.spec import ABIContractMethod, ABIStruct, ContractMethod, get_contract_methods

ESCAPED_QUOTE = r"\""


@dataclasses.dataclass(kw_only=True)
class GenerationSettings:
    indent: str = "    "
    max_line_length: int = 80

    @property
    def indent_length(self) -> int:
        return len(self.indent)


class GenerateContext:
    def __init__(self, app_spec: algokit_utils.ApplicationSpecification):
        self.app_spec = app_spec
        # TODO: track these as they are emitted?
        self.used_module_symbols = {
            "_APP_SPEC_JSON",
            "APP_SPEC",
            "_TArgs",
            "_TArgsHolder",
            "_TResult",
            "_ArgsBase",
            "_as_dict",
            "_filter_none",
            "_convert_on_complete",
            "_convert_deploy_args",
            "DeployCreate",
            "Deploy",
            "GlobalState",
            "LocalState",
            "Composer",
        }
        self.used_client_symbols = {
            "__init__",
            "app_spec",
            "app_client",
            "algod_client",
            "app_id",
            "app_address",
            "sender",
            "signer",
            "suggested_params",
            "no_op",
            "clear_state",
            "deploy",
            "get_global_state",
            "get_local_state",
            "compose",
        }
        self.client_name = utils.get_unique_symbol_by_incrementing(
            self.used_module_symbols, utils.get_class_name(self.app_spec.contract.name, "client")
        )
        self.methods = get_contract_methods(app_spec, self.used_module_symbols, self.used_client_symbols)
        self.disable_linting = True


def generated_comment(context: GenerateContext) -> DocumentParts:
    yield "# This file was automatically generated by algokit-client-generator."
    yield "# DO NOT MODIFY IT BY HAND."
    yield "# requires: algokit-utils@^1.2.0"


def disable_linting(context: GenerateContext) -> DocumentParts:
    yield "# flake8: noqa"  # this works for flake8 and ruff
    yield "# fmt: off"  # disable formatting
    yield '# mypy: disable-error-code="no-any-return, no-untyped-call"'  # disable common type warnings


def imports(context: GenerateContext) -> DocumentParts:
    yield utils.lines(
        """import base64
import dataclasses
import decimal
import typing
from abc import ABC, abstractmethod

import algokit_utils
import algosdk
from algosdk.atomic_transaction_composer import (
    AtomicTransactionComposer,
    AtomicTransactionResponse,
    TransactionSigner,
    TransactionWithSigner
)"""
    )


def typed_argument_class(abi: ABIContractMethod) -> DocumentParts:
    assert abi
    yield "@dataclasses.dataclass(kw_only=True)"
    yield f"class {abi.args_class_name}(_ArgsBase[{abi.python_type}]):"
    yield Part.IncIndent
    if abi.method.desc:
        yield utils.docstring(abi.method.desc)
        yield Part.Gap1
    if abi.args:
        for arg in abi.args:
            yield Part.InlineMode
            yield f"{arg.name}: {arg.python_type}"
            if arg.has_default:
                yield " | None = None"
            yield Part.RestoreLineMode
            if arg.desc:
                yield utils.docstring(arg.desc)
        yield Part.Gap1
    yield "@staticmethod"
    yield "def method() -> str:"
    yield Part.IncIndent
    yield Part.InlineMode
    yield "return "
    yield utils.string_literal(abi.method.get_signature())
    yield Part.DecIndent
    yield Part.DecIndent
    yield Part.RestoreLineMode


def helpers(context: GenerateContext) -> DocumentParts:
    has_abi_create = any(m.abi for m in context.methods.create)
    has_abi_update = any(m.abi for m in context.methods.update_application)
    has_abi_delete = any(m.abi for m in context.methods.delete_application)
    if context.methods.has_abi_methods:
        yield '_TReturn = typing.TypeVar("_TReturn")'
        yield Part.Gap2
        yield utils.indented(
            """
class _ArgsBase(ABC, typing.Generic[_TReturn]):
    @staticmethod
    @abstractmethod
    def method() -> str:
        ..."""
        )
    yield Part.Gap2
    yield '_TArgs = typing.TypeVar("_TArgs", bound=_ArgsBase[typing.Any])'
    yield Part.Gap2
    yield utils.indented(
        """
@dataclasses.dataclass(kw_only=True)
class _TArgsHolder(typing.Generic[_TArgs]):
    args: _TArgs
"""
    )
    yield Part.Gap2

    if has_abi_create:
        yield utils.indented(
            """
@dataclasses.dataclass(kw_only=True)
class DeployCreate(algokit_utils.DeployCreateCallArgs, _TArgsHolder[_TArgs], typing.Generic[_TArgs]):
    pass
"""
        )
        yield Part.Gap2
    if has_abi_update or has_abi_delete:
        yield utils.indented(
            """
@dataclasses.dataclass(kw_only=True)
class Deploy(algokit_utils.DeployCallArgs, _TArgsHolder[_TArgs], typing.Generic[_TArgs]):
    pass"""
        )
        yield Part.Gap2

    yield Part.Gap2
    yield utils.indented(
        """
def _filter_none(value: dict | typing.Any) -> dict | typing.Any:
    if isinstance(value, dict):
        return {k: _filter_none(v) for k, v in value.items() if v is not None}
    return value"""
    )
    yield Part.Gap2
    yield utils.indented(
        """
def _as_dict(data: typing.Any, *, convert_all: bool = True) -> dict[str, typing.Any]:
    if data is None:
        return {}
    if not dataclasses.is_dataclass(data):
        raise TypeError(f"{data} must be a dataclass")
    if convert_all:
        result = dataclasses.asdict(data)
    else:
        result = {f.name: getattr(data, f.name) for f in dataclasses.fields(data)}
    return _filter_none(result)"""
    )
    yield Part.Gap2
    yield utils.indented(
        """
def _convert_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
) -> algokit_utils.CommonCallParametersDict:
    return typing.cast(algokit_utils.CommonCallParametersDict, _as_dict(transaction_parameters))"""
    )
    yield Part.Gap2
    yield utils.indented(
        """
def _convert_call_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
) -> algokit_utils.OnCompleteCallParametersDict:
    return typing.cast(algokit_utils.OnCompleteCallParametersDict, _as_dict(transaction_parameters))"""
    )
    yield Part.Gap2
    yield utils.indented(
        """
def _convert_create_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
    on_complete: algokit_utils.OnCompleteActionName,
) -> algokit_utils.CreateCallParametersDict:
    result = typing.cast(algokit_utils.CreateCallParametersDict, _as_dict(transaction_parameters))
    on_complete_enum = on_complete.replace("_", " ").title().replace(" ", "") + "OC"
    result["on_complete"] = getattr(algosdk.transaction.OnComplete, on_complete_enum)
    return result
    """
    )
    yield Part.Gap2
    yield utils.indented(
        """
def _convert_deploy_args(
    deploy_args: algokit_utils.DeployCallArgs | None,
) -> algokit_utils.ABICreateCallArgsDict | None:
    if deploy_args is None:
        return None

    deploy_args_dict = typing.cast(algokit_utils.ABICreateCallArgsDict, _as_dict(deploy_args))
    if isinstance(deploy_args, _TArgsHolder):
        deploy_args_dict["args"] = _as_dict(deploy_args.args)
        deploy_args_dict["method"] = deploy_args.args.method()

    return deploy_args_dict"""
    )
    yield Part.Gap2


def named_struct(context: GenerateContext, struct: ABIStruct) -> DocumentParts:
    yield "@dataclasses.dataclass(kw_only=True)"
    yield f"class {struct.struct_class_name}:"
    yield Part.IncIndent
    for field in struct.fields:
        yield f"{field.name}: {field.python_type}"
    yield Part.DecIndent


def typed_arguments(context: GenerateContext) -> DocumentParts:
    # typed args classes
    processed_abi_signatures: set[str] = set()
    processed_abi_structs: set[str] = set()
    for method in context.methods.all_abi_methods:
        abi = method.abi
        assert abi
        abi_signature = abi.method.get_signature()
        if abi_signature in processed_abi_signatures:
            continue
        for struct in abi.structs:
            if struct.struct_class_name not in processed_abi_structs:
                yield named_struct(context, struct)
                yield Part.Gap2
                processed_abi_structs.add(struct.struct_class_name)

        processed_abi_signatures.add(abi_signature)
        yield typed_argument_class(abi)
        yield Part.Gap2

    yield Part.Gap2


def state_type(context: GenerateContext, class_name: str, schema: dict[str, dict]) -> DocumentParts:
    if not schema:
        return

    yield f"class {class_name}:"
    yield Part.IncIndent
    yield "def __init__(self, data: dict[bytes, bytes | int]):"
    yield Part.IncIndent
    for field, value in schema.items():
        key = value["key"]
        if value["type"] == "bytes":
            yield f'self.{field} = ByteReader(typing.cast(bytes, data.get(b"{key}")))'
        else:
            yield f'self.{field} = typing.cast(int, data.get(b"{key}"))'
        desc = value["descr"]
        if desc:
            yield utils.docstring(desc)
    yield Part.DecIndent
    yield Part.DecIndent
    yield Part.Gap2


def _get_declared_schema(
    app_spec: algokit_utils.ApplicationSpecification, schema_name: Literal["global", "local"]
) -> dict[str, dict[str, typing.Any]]:
    schema = app_spec.schema.get(schema_name) or {}
    return schema.get("declared") or {}


def state_types(context: GenerateContext) -> DocumentParts:
    app_spec = context.app_spec
    global_schema = _get_declared_schema(app_spec, "global")
    local_schema = _get_declared_schema(app_spec, "local")
    has_bytes = any(i.get("type") == "bytes" for i in [*global_schema.values(), *local_schema.values()])
    if has_bytes:
        yield utils.indented(
            """
class ByteReader:
    def __init__(self, data: bytes):
        self._data = data

    @property
    def as_bytes(self) -> bytes:
        return self._data

    @property
    def as_str(self) -> str:
        return self._data.decode("utf8")

    @property
    def as_base64(self) -> str:
        return base64.b64encode(self._data).decode("utf8")

    @property
    def as_hex(self) -> str:
        return self._data.hex()"""
        )
        yield Part.Gap2
    yield state_type(context, "GlobalState", global_schema)
    yield state_type(context, "LocalState", local_schema)


def composer(context: GenerateContext) -> DocumentParts:
    yield utils.indented(
        """
class Composer:

    def __init__(self, app_client: algokit_utils.ApplicationClient, atc: AtomicTransactionComposer):
        self.app_client = app_client
        self.atc = atc

    def build(self) -> AtomicTransactionComposer:
        return self.atc

    def execute(self) -> AtomicTransactionResponse:
        return self.app_client.execute_atc(self.atc)
"""
    )
    yield Part.IncIndent
    yield Part.Gap1
    yield methods_by_side_effect(context, "none", context.methods.no_op, is_compose_method=True)
    yield Part.Gap1
    yield methods_by_side_effect(context, "create", context.methods.create, is_compose_method=True)
    yield Part.Gap1
    yield methods_by_side_effect(context, "update", context.methods.update_application, is_compose_method=True)
    yield Part.Gap1
    yield methods_by_side_effect(context, "delete", context.methods.delete_application, is_compose_method=True)
    yield Part.Gap1
    yield methods_by_side_effect(context, "opt_in", context.methods.opt_in, is_compose_method=True)
    yield Part.Gap1
    yield methods_by_side_effect(context, "close_out", context.methods.close_out, is_compose_method=True)
    yield Part.Gap1
    yield compose_clear_method(context)
    yield Part.DecIndent


def typed_client(context: GenerateContext) -> DocumentParts:
    yield f"class {context.client_name}:"
    yield Part.IncIndent
    yield utils.docstring(
        (f"{context.app_spec.contract.desc}\n\n" if context.app_spec.contract.desc else "")
        + f"""A class for interacting with the {context.app_spec.contract.name} app providing high productivity and
strongly typed methods to deploy and call the app"""
    )
    yield Part.Gap1
    yield utils.indented(
        """
@typing.overload
def __init__(
    self,
    algod_client: algosdk.v2client.algod.AlgodClient,
    *,
    app_id: int = 0,
    signer: TransactionSigner | algokit_utils.Account | None = None,
    sender: str | None = None,
    suggested_params: algosdk.transaction.SuggestedParams | None = None,
    template_values: algokit_utils.TemplateValueMapping | None = None,
    app_name: str | None = None,
) -> None:
    ..."""
    )
    yield Part.Gap1
    yield utils.indented(
        """
@typing.overload
def __init__(
    self,
    algod_client: algosdk.v2client.algod.AlgodClient,
    *,
    creator: str | algokit_utils.Account,
    indexer_client: algosdk.v2client.indexer.IndexerClient | None = None,
    existing_deployments: algokit_utils.AppLookup | None = None,
    signer: TransactionSigner | algokit_utils.Account | None = None,
    sender: str | None = None,
    suggested_params: algosdk.transaction.SuggestedParams | None = None,
    template_values: algokit_utils.TemplateValueMapping | None = None,
    app_name: str | None = None,
) -> None:
    ..."""
    )
    yield Part.Gap1
    yield utils.indented(
        """
def __init__(
    self,
    algod_client: algosdk.v2client.algod.AlgodClient,
    *,
    creator: str | algokit_utils.Account | None = None,
    indexer_client: algosdk.v2client.indexer.IndexerClient | None = None,
    existing_deployments: algokit_utils.AppLookup | None = None,
    app_id: int = 0,
    signer: TransactionSigner | algokit_utils.Account | None = None,
    sender: str | None = None,
    suggested_params: algosdk.transaction.SuggestedParams | None = None,
    template_values: algokit_utils.TemplateValueMapping | None = None,
    app_name: str | None = None,
) -> None:"""
    )
    yield Part.IncIndent
    yield utils.docstring(
        f"""
{context.client_name} can be created with an app_id to interact with an existing application, alternatively
it can be created with a creator and indexer_client specified to find existing applications by name and creator.

:param AlgodClient algod_client: AlgoSDK algod client
:param int app_id: The app_id of an existing application, to instead find the application by creator and name
use the creator and indexer_client parameters
:param str | Account creator: The address or Account of the app creator to resolve the app_id
:param IndexerClient indexer_client: AlgoSDK indexer client, only required if deploying or finding app_id by
creator and app name
:param AppLookup existing_deployments:
:param TransactionSigner | Account signer: Account or signer to use to sign transactions, if not specified and
creator was passed as an Account will use that.
:param str sender: Address to use as the sender for all transactions, will use the address associated with the
signer if not specified.
:param TemplateValueMapping template_values: Values to use for TMPL_* template variables, dictionary keys should
*NOT* include the TMPL_ prefix
:param str | None app_name: Name of application to use when deploying, defaults to name defined on the
Application Specification
    """
    )
    yield Part.Gap1
    yield utils.indented(
        """
self.app_spec = APP_SPEC

# calling full __init__ signature, so ignoring mypy warning about overloads
self.app_client = algokit_utils.ApplicationClient(  # type: ignore[call-overload, misc]
    algod_client=algod_client,
    app_spec=self.app_spec,
    app_id=app_id,
    creator=creator,
    indexer_client=indexer_client,
    existing_deployments=existing_deployments,
    signer=signer,
    sender=sender,
    suggested_params=suggested_params,
    template_values=template_values,
    app_name=app_name,
)"""
    )
    yield Part.Gap1
    yield Part.DecIndent
    yield forwarded_client_properties(context)
    yield Part.Gap1
    if _get_declared_schema(context.app_spec, "global"):
        yield get_global_state_method(context)
        yield Part.Gap1
    if _get_declared_schema(context.app_spec, "local"):
        yield get_local_state_method(context)
        yield Part.Gap1
    yield methods_by_side_effect(context, "none", context.methods.no_op)
    yield Part.Gap1
    yield methods_by_side_effect(context, "create", context.methods.create)
    yield Part.Gap1
    yield methods_by_side_effect(context, "update", context.methods.update_application)
    yield Part.Gap1
    yield methods_by_side_effect(context, "delete", context.methods.delete_application)
    yield Part.Gap1
    yield methods_by_side_effect(context, "opt_in", context.methods.opt_in)
    yield Part.Gap1
    yield methods_by_side_effect(context, "close_out", context.methods.close_out)
    yield Part.Gap1
    yield clear_method(context)
    yield Part.Gap1
    yield deploy_method(context)
    yield Part.Gap1
    yield compose_method()


def forwarded_client_properties(context: GenerateContext) -> DocumentParts:
    yield utils.indented(
        """
@property
def algod_client(self) -> algosdk.v2client.algod.AlgodClient:
    return self.app_client.algod_client"""
    )
    yield Part.Gap1
    yield utils.indented(
        """
@property
def app_id(self) -> int:
    return self.app_client.app_id"""
    )
    yield Part.Gap1
    yield utils.indented(
        """
@app_id.setter
def app_id(self, value: int) -> None:
    self.app_client.app_id = value"""
    )
    yield Part.Gap1
    yield utils.indented(
        """
@property
def app_address(self) -> str:
    return self.app_client.app_address"""
    )
    yield Part.Gap1
    yield utils.indented(
        """
@property
def sender(self) -> str | None:
    return self.app_client.sender"""
    )
    yield Part.Gap1
    yield utils.indented(
        """
@sender.setter
def sender(self, value: str) -> None:
    self.app_client.sender = value"""
    )
    yield Part.Gap1
    yield utils.indented(
        """
@property
def signer(self) -> TransactionSigner | None:
    return self.app_client.signer"""
    )
    yield Part.Gap1
    yield utils.indented(
        """
@signer.setter
def signer(self, value: TransactionSigner) -> None:
    self.app_client.signer = value"""
    )
    yield Part.Gap1
    yield utils.indented(
        """
@property
def suggested_params(self) -> algosdk.transaction.SuggestedParams | None:
    return self.app_client.suggested_params"""
    )
    yield Part.Gap1
    yield utils.indented(
        """
@suggested_params.setter
def suggested_params(self, value: algosdk.transaction.SuggestedParams | None) -> None:
    self.app_client.suggested_params = value"""
    )


def embed_app_spec(context: GenerateContext) -> DocumentParts:
    yield Part.InlineMode
    yield '_APP_SPEC_JSON = r"""'
    yield context.app_spec.to_json()
    yield '"""'
    yield Part.RestoreLineMode
    yield "APP_SPEC = algokit_utils.ApplicationSpecification.from_json(_APP_SPEC_JSON)"


def abi_method_doc_string(method: ContractMethod, *, compose_signature: bool) -> Iterable[str]:
    assert method.abi
    if method.abi.method.desc:
        yield method.abi.method.desc
        yield ""
    if compose_signature:
        yield f"Adds a call to `{method.abi.method.get_signature()}` ABI method"
    else:
        yield f"Calls `{method.abi.method.get_signature()}` ABI method"
    yield ""
    for arg in method.abi.args:
        desc = f":param {arg.python_type} {arg.name}: "
        desc += "(optional) " if arg.has_default else ""
        desc += arg.desc or f"The `{arg.name}` ABI parameter"
        yield desc
    if method.call_config == "create":
        on_completes = method.on_complete
        yield f":param typing.Literal[{', '.join(on_completes)}] on_complete: On completion type to use"
        yield (
            ":param algokit_utils.CreateTransactionParameters transaction_parameters: "
            "(optional) Additional transaction parameters"
        )
    else:
        yield (
            ":param algokit_utils.TransactionParameters transaction_parameters: "
            "(optional) Additional transaction parameters"
        )
    if compose_signature:
        yield ":returns Composer: This Composer instance"
    else:
        yield (
            f":returns algokit_utils.ABITransactionResponse[{method.abi.python_type}]: "
            f"{method.abi.method.returns.desc or 'The result of the transaction'}"
        )


def bare_method_doc_string(method: ContractMethod, *, compose_signature: bool) -> Iterable[str]:
    if method.call_config == "create":
        if compose_signature and len(method.on_complete) > 1:
            yield f"Adds a call to create an application using one of the {', '.join(method.on_complete)} bare methods"
        elif compose_signature:
            yield f"Adds a call to create an application using the {method.on_complete[0]} bare method"
        elif len(method.on_complete) > 1:
            yield f"Creates an application using one of the {', '.join(method.on_complete)} bare methods"
        else:
            yield f"Creates an application using the {method.on_complete[0]} bare method"
        yield ""
        on_completes = method.on_complete
        yield f":param typing.Literal[{', '.join(on_completes)}] on_complete: On completion type to use"
        yield (
            ":param algokit_utils.CreateTransactionParameters transaction_parameters: "
            "(optional) Additional transaction parameters"
        )
    else:
        if compose_signature:
            yield f"Adds a calls to the {method.on_complete[0]} bare method"
        else:
            yield f"Calls the {method.on_complete[0]} bare method"
        yield ""
        yield (
            ":param algokit_utils.TransactionParameters transaction_parameters: "
            "(optional) Additional transaction parameters"
        )
    if compose_signature:
        yield ":returns Composer: This Composer instance"
    else:
        yield ":returns algokit_utils.TransactionResponse: The result of the transaction"


def create_method_doc_string(method: ContractMethod, *, compose_signature: bool) -> Iterable[str]:
    if method.abi:
        return abi_method_doc_string(method, compose_signature=compose_signature)
    else:
        return bare_method_doc_string(method, compose_signature=compose_signature)


def signature(
    context: GenerateContext, name: str, method: ContractMethod, *, compose_signature: bool = False
) -> DocumentParts:
    yield f"def {name}("
    yield Part.IncIndent
    yield "self,"
    yield "*,"
    abi = method.abi
    if abi:
        for arg in abi.args:
            if arg.has_default:
                yield f"{arg.name}: {arg.python_type} | None = None,"
            else:
                yield f"{arg.name}: {arg.python_type},"
    if method.call_config == "create":
        yield on_complete_literals(method.on_complete)
        yield "transaction_parameters: algokit_utils.CreateTransactionParameters | None = None,"
    else:
        yield "transaction_parameters: algokit_utils.TransactionParameters | None = None,"
    yield Part.DecIndent

    if compose_signature:
        return_type = '"Composer"'
    elif abi:
        return_type = f"algokit_utils.ABITransactionResponse[{abi.python_type}]"
    else:
        return_type = "algokit_utils.TransactionResponse"
    yield f") -> {return_type}:"
    yield Part.IncIndent
    yield utils.docstring("\n".join(create_method_doc_string(method, compose_signature=compose_signature)))
    yield Part.DecIndent
    yield Part.Gap1


def instantiate_args(contract_method: ABIContractMethod | None) -> DocumentParts:
    if contract_method and not contract_method.args:
        yield f"args = {contract_method.args_class_name}()"
    elif contract_method:
        yield f"args = {contract_method.args_class_name}(", Part.IncIndent
        for arg in contract_method.args:
            yield f"{arg.name}={arg.name},"
        yield Part.DecIndent, ")"


def app_client_call(
    app_client_method: Literal["call", "create", "update", "delete", "opt_in", "close_out"],
    contract_method: ContractMethod,
) -> DocumentParts:
    yield f"result = self.app_client.{app_client_method}("
    yield Part.IncIndent
    if contract_method.abi:
        yield "call_abi_method=args.method(),"
    else:
        yield "call_abi_method=False,"
    if contract_method.call_config == "create":
        yield "transaction_parameters=_convert_create_transaction_parameters(transaction_parameters, on_complete),"
    elif "no_op" in contract_method.on_complete:
        yield "transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),"
    else:
        yield "transaction_parameters=_convert_transaction_parameters(transaction_parameters),"
    if contract_method.abi:
        yield "**_as_dict(args, convert_all=True),"
    yield Part.DecIndent
    yield ")"
    if contract_method.abi and contract_method.abi.result_struct:
        yield 'elements = self.app_spec.hints[args.method()].structs["output"]["elements"]'
        yield "result_dict = {element[0]: value for element, value in zip(elements, result.return_value)}"
        yield f"result.return_value = {contract_method.abi.python_type}(**result_dict)"
    yield "return result"


def app_client_compose_call(
    app_client_method: Literal["call", "create", "update", "delete", "opt_in", "close_out"],
    contract_method: ContractMethod,
) -> DocumentParts:
    yield f"self.app_client.compose_{app_client_method}("
    yield Part.IncIndent
    yield "self.atc,"
    if contract_method.abi:
        yield "call_abi_method=args.method(),"
    else:
        yield "call_abi_method=False,"
    if contract_method.call_config == "create":
        yield "transaction_parameters=_convert_create_transaction_parameters(transaction_parameters, on_complete),"
    elif "no_op" in contract_method.on_complete:
        yield "transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),"
    else:
        yield "transaction_parameters=_convert_transaction_parameters(transaction_parameters),"
    if contract_method.abi:
        yield "**_as_dict(args, convert_all=True),"
    yield Part.DecIndent
    yield ")"
    yield "return self"


def on_complete_literals(on_completes: Iterable[algokit_utils.OnCompleteActionName]) -> DocumentParts:
    yield Part.InlineMode
    yield 'on_complete: typing.Literal["'
    yield utils.join('", "', on_completes)
    yield '"]'
    if "no_op" in on_completes:
        yield ' = "no_op"'
    yield ","
    yield Part.RestoreLineMode


def methods_by_side_effect(
    context: GenerateContext,
    side_effect: Literal["none", "create", "update", "delete", "opt_in", "close_out"],
    methods: list[ContractMethod],
    *,
    is_compose_method: bool = False,
) -> DocumentParts:
    if not methods:
        return

    for method in methods:
        contract_method = method.abi

        if side_effect == "none":
            if contract_method:  # an ABI method with no_op=CALL method
                full_method_name = contract_method.client_method_name
            else:
                full_method_name = "no_op"
        elif contract_method:  # an ABI method with a side effect
            full_method_name = f"{side_effect}_{contract_method.client_method_name}"
        else:  # a bare method
            full_method_name = f"{side_effect}_bare"
        yield signature(context, full_method_name, method, compose_signature=is_compose_method)
        yield Part.IncIndent
        yield instantiate_args(contract_method)
        if is_compose_method:
            yield app_client_compose_call("call" if side_effect == "none" else side_effect, method)
        else:
            yield app_client_call("call" if side_effect == "none" else side_effect, method)
        yield Part.DecIndent
        yield Part.Gap1


def clear_method(context: GenerateContext) -> DocumentParts:
    yield utils.indented(
        """
def clear_state(
    self,
    transaction_parameters: algokit_utils.TransactionParameters | None = None,
    app_args: list[bytes] | None = None,
) -> algokit_utils.TransactionResponse:
    \"""Calls the application with on completion set to ClearState

    :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
    :param list[bytes] | None app_args: (optional) Application args to pass
    :returns algokit_utils.TransactionResponse: The result of the transaction\"""

    return self.app_client.clear_state(_convert_transaction_parameters(transaction_parameters), app_args)"""
    )


def compose_clear_method(context: GenerateContext) -> DocumentParts:
    yield utils.indented(
        """
def clear_state(
    self,
    transaction_parameters: algokit_utils.TransactionParameters | None = None,
    app_args: list[bytes] | None = None,
) -> "Composer":
    \"""Adds a call to the application with on completion set to ClearState

    :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
    :param list[bytes] | None app_args: (optional) Application args to pass\"""

    self.app_client.compose_clear_state(self.atc, _convert_transaction_parameters(transaction_parameters), app_args)
    return self
"""
    )


def deploy_method_args_type(arg_name: str, methods: list[ContractMethod]) -> str:
    has_bare = any(not m.abi for m in methods) or not methods
    typed_args = [m.abi.args_class_name for m in methods if m.abi]
    args = []
    if typed_args:
        deploy_type = "DeployCreate" if arg_name == "create_args" else "Deploy"
        args.append(f"{deploy_type}[{' | '.join(typed_args)}]")
    if has_bare:
        args.append("algokit_utils.DeployCallArgs")
        args.append("None")

    return " | ".join(args)


def deploy_method_args(context: GenerateContext, arg_name: str, methods: list[ContractMethod]) -> DocumentParts:
    yield Part.InlineMode

    yield f"{arg_name}: "
    yield deploy_method_args_type(arg_name, methods)
    if any(not m.abi for m in methods) or not methods:
        yield " = None"
    yield ","
    yield Part.RestoreLineMode


def deploy_method(context: GenerateContext) -> DocumentParts:
    yield utils.indented(
        """
def deploy(
    self,
    version: str | None = None,
    *,
    signer: TransactionSigner | None = None,
    sender: str | None = None,
    allow_update: bool | None = None,
    allow_delete: bool | None = None,
    on_update: algokit_utils.OnUpdate = algokit_utils.OnUpdate.Fail,
    on_schema_break: algokit_utils.OnSchemaBreak = algokit_utils.OnSchemaBreak.Fail,
    template_values: algokit_utils.TemplateValueMapping | None = None,"""
    )
    yield Part.IncIndent
    yield deploy_method_args(context, "create_args", context.methods.create)
    yield deploy_method_args(context, "update_args", context.methods.update_application)
    yield deploy_method_args(context, "delete_args", context.methods.delete_application)
    yield Part.DecIndent
    yield utils.indented(
        """
) -> algokit_utils.DeployResponse:"""
    )
    yield Part.IncIndent

    create_args_type = deploy_method_args_type("create_args", context.methods.create)
    update_args_type = deploy_method_args_type("update_args", context.methods.update_application)
    delete_args_type = deploy_method_args_type("delete_args", context.methods.delete_application)
    yield utils.docstring(
        f"""Deploy an application and update client to reference it.

Idempotently deploy (create, update/delete if changed) an app against the given name via the given creator
account, including deploy-time template placeholder substitutions.
To understand the architecture decisions behind this functionality please see
<https://github.com/algorandfoundation/algokit-cli/blob/main/docs/architecture-decisions/2023-01-12_smart-contract-deployment.md>

```{{note}}
If there is a breaking state schema change to an existing app (and `on_schema_break` is set to
'ReplaceApp' the existing app will be deleted and re-created.
```

```{{note}}
If there is an update (different TEAL code) to an existing app (and `on_update` is set to 'ReplaceApp')
the existing app will be deleted and re-created.
```

:param str version: version to use when creating or updating app, if None version will be auto incremented
:param algosdk.atomic_transaction_composer.TransactionSigner signer: signer to use when deploying app
, if None uses self.signer
:param str sender: sender address to use when deploying app, if None uses self.sender
:param bool allow_delete: Used to set the `TMPL_DELETABLE` template variable to conditionally control if an app
can be deleted
:param bool allow_update: Used to set the `TMPL_UPDATABLE` template variable to conditionally control if an app
can be updated
:param OnUpdate on_update: Determines what action to take if an application update is required
:param OnSchemaBreak on_schema_break: Determines what action to take if an application schema requirements
has increased beyond the current allocation
:param dict[str, int|str|bytes] template_values: Values to use for `TMPL_*` template variables, dictionary keys
should *NOT* include the TMPL_ prefix
:param {create_args_type} create_args: Arguments used when creating an application
:param {update_args_type} update_args: Arguments used when updating an application
:param {delete_args_type} delete_args: Arguments used when deleting an application
:return DeployResponse: details action taken and relevant transactions
:raises DeploymentError: If the deployment failed"""
    )
    yield Part.Gap1
    yield utils.indented(
        """
return self.app_client.deploy(
    version,
    signer=signer,
    sender=sender,
    allow_update=allow_update,
    allow_delete=allow_delete,
    on_update=on_update,
    on_schema_break=on_schema_break,
    template_values=template_values,
    create_args=_convert_deploy_args(create_args),
    update_args=_convert_deploy_args(update_args),
    delete_args=_convert_deploy_args(delete_args),
)"""
    )
    yield Part.DecIndent


def compose_method() -> DocumentParts:
    yield utils.indented(
        """
def compose(self, atc: AtomicTransactionComposer | None = None) -> Composer:
    return Composer(self.app_client, atc or AtomicTransactionComposer())"""
    )


def get_global_state_method(context: GenerateContext) -> DocumentParts:
    if not context.app_spec.schema.get("global", {}).get("declared", {}):
        return
    yield "def get_global_state(self) -> GlobalState:"
    yield Part.IncIndent
    yield utils.docstring(
        "Returns the application's global state wrapped in a strongly typed class"
        " with options to format the stored value"
    )
    yield Part.Gap1
    yield "state = typing.cast(dict[bytes, bytes | int], self.app_client.get_global_state(raw=True))"
    yield "return GlobalState(state)"
    yield Part.DecIndent


def get_local_state_method(context: GenerateContext) -> DocumentParts:
    if not context.app_spec.schema.get("local", {}).get("declared", {}):
        return
    yield "def get_local_state(self, account: str | None = None) -> LocalState:"
    yield Part.IncIndent
    yield utils.docstring(
        "Returns the application's local state wrapped in a strongly typed class"
        " with options to format the stored value"
    )
    yield Part.Gap1
    yield "state = typing.cast(dict[bytes, bytes | int], self.app_client.get_local_state(account, raw=True))"
    yield "return LocalState(state)"
    yield Part.DecIndent


def generate(context: GenerateContext) -> DocumentParts:
    if context.disable_linting:
        yield disable_linting(context)
    yield generated_comment(context)
    yield imports(context)
    yield Part.Gap1
    yield embed_app_spec(context)
    yield helpers(context)
    yield Part.Gap2
    yield typed_arguments(context)
    yield Part.Gap2
    yield state_types(context)
    yield Part.Gap2
    yield composer(context)
    yield Part.Gap2
    yield typed_client(context)
