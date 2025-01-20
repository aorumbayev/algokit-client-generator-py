# flake8: noqa
# fmt: off
# mypy: disable-error-code="no-any-return, no-untyped-call, misc, type-arg"
# This file was automatically generated by algokit-client-generator.
# DO NOT MODIFY IT BY HAND.
# requires: algokit-utils@^3.0.0

# common
import dataclasses
import typing
# core algosdk
import algosdk
from algosdk.transaction import OnComplete
from algosdk.atomic_transaction_composer import TransactionWithSigner
from algosdk.atomic_transaction_composer import TransactionSigner
from algosdk.source_map import SourceMap
from algosdk.transaction import Transaction
from algosdk.v2client.models import SimulateTraceConfig
# utils
from algokit_utils import applications, models, protocols, transactions
from algokit_utils.applications import abi as applications_abi

_APP_SPEC_JSON = r"""{
    "arcs": [],
    "bareActions": {
        "call": [
            "DeleteApplication",
            "UpdateApplication"
        ],
        "create": [
            "NoOp"
        ]
    },
    "methods": [],
    "name": "App",
    "state": {
        "keys": {
            "box": {},
            "global": {},
            "local": {}
        },
        "maps": {
            "box": {},
            "global": {},
            "local": {}
        },
        "schema": {
            "global": {
                "bytes": 0,
                "ints": 0
            },
            "local": {
                "bytes": 0,
                "ints": 0
            }
        }
    },
    "structs": {},
    "desc": "An app that has no abi methods",
    "source": {
        "approval": "I3ByYWdtYSB2ZXJzaW9uIDgKaW50Y2Jsb2NrIDAgMQp0eG4gTnVtQXBwQXJncwppbnRjXzAgLy8gMAo9PQpibnogbWFpbl9sMgplcnIKbWFpbl9sMjoKdHhuIE9uQ29tcGxldGlvbgppbnRjXzAgLy8gTm9PcAo9PQpibnogbWFpbl9sOAp0eG4gT25Db21wbGV0aW9uCnB1c2hpbnQgNCAvLyBVcGRhdGVBcHBsaWNhdGlvbgo9PQpibnogbWFpbl9sNwp0eG4gT25Db21wbGV0aW9uCnB1c2hpbnQgNSAvLyBEZWxldGVBcHBsaWNhdGlvbgo9PQpibnogbWFpbl9sNgplcnIKbWFpbl9sNjoKdHhuIEFwcGxpY2F0aW9uSUQKaW50Y18wIC8vIDAKIT0KYXNzZXJ0CmNhbGxzdWIgZGVsZXRlXzEKaW50Y18xIC8vIDEKcmV0dXJuCm1haW5fbDc6CnR4biBBcHBsaWNhdGlvbklECmludGNfMCAvLyAwCiE9CmFzc2VydApjYWxsc3ViIHVwZGF0ZV8wCmludGNfMSAvLyAxCnJldHVybgptYWluX2w4Ogp0eG4gQXBwbGljYXRpb25JRAppbnRjXzAgLy8gMAo9PQphc3NlcnQKaW50Y18xIC8vIDEKcmV0dXJuCgovLyB1cGRhdGUKdXBkYXRlXzA6CnByb3RvIDAgMAp0eG4gU2VuZGVyCmdsb2JhbCBDcmVhdG9yQWRkcmVzcwo9PQovLyB1bmF1dGhvcml6ZWQKYXNzZXJ0CnB1c2hpbnQgVE1QTF9VUERBVEFCTEUgLy8gVE1QTF9VUERBVEFCTEUKLy8gQ2hlY2sgYXBwIGlzIHVwZGF0YWJsZQphc3NlcnQKcmV0c3ViCgovLyBkZWxldGUKZGVsZXRlXzE6CnByb3RvIDAgMAp0eG4gU2VuZGVyCmdsb2JhbCBDcmVhdG9yQWRkcmVzcwo9PQovLyB1bmF1dGhvcml6ZWQKYXNzZXJ0CnB1c2hpbnQgVE1QTF9ERUxFVEFCTEUgLy8gVE1QTF9ERUxFVEFCTEUKLy8gQ2hlY2sgYXBwIGlzIGRlbGV0YWJsZQphc3NlcnQKcmV0c3Vi",
        "clear": "I3ByYWdtYSB2ZXJzaW9uIDgKcHVzaGludCAwIC8vIDAKcmV0dXJu"
    }
}"""
APP_SPEC = applications.Arc56Contract.from_json(_APP_SPEC_JSON)

def _parse_abi_args(args: typing.Any | None = None) -> list[typing.Any] | None:
    """Helper to parse ABI args into the format expected by underlying client"""
    if args is None:
        return None

    def convert_dataclass(value: typing.Any) -> typing.Any:
        if dataclasses.is_dataclass(value):
            return tuple(convert_dataclass(getattr(value, field.name)) for field in dataclasses.fields(value))
        elif isinstance(value, (list, tuple)):
            return type(value)(convert_dataclass(item) for item in value)
        return value

    match args:
        case tuple():
            method_args = list(args)
        case _ if dataclasses.is_dataclass(args):
            method_args = [getattr(args, field.name) for field in dataclasses.fields(args)]
        case _:
            raise ValueError("Invalid 'args' type. Expected 'tuple' or 'TypedDict' for respective typed arguments.")

    return [convert_dataclass(arg) for arg in method_args] if method_args else None


class _AppUpdate:
    def __init__(self, app_client: applications.AppClient):
        self.app_client = app_client

    def bare(self, params: applications.AppClientBareCallWithCompilationAndSendParams | None = None) -> transactions.AppUpdateParams:
        return self.app_client.params.bare.update(params)


class _AppDelete:
    def __init__(self, app_client: applications.AppClient):
        self.app_client = app_client

    def bare(self, params: applications.AppClientBareCallWithSendParams | None = None) -> transactions.AppCallParams:
        return self.app_client.params.bare.delete(params)


class AppParams:
    def __init__(self, app_client: applications.AppClient):
        self.app_client = app_client
    @property
    def update(self) -> "_AppUpdate":
        return _AppUpdate(self.app_client)

    @property
    def delete(self) -> "_AppDelete":
        return _AppDelete(self.app_client)

    def clear_state(self, params: applications.AppClientBareCallWithSendParams | None = None) -> transactions.AppCallParams:
        return self.app_client.params.bare.clear_state(params)


class _AppUpdateTransaction:
    def __init__(self, app_client: applications.AppClient):
        self.app_client = app_client

    def bare(self, params: applications.AppClientBareCallWithCompilationAndSendParams | None = None) -> Transaction:
        return self.app_client.create_transaction.bare.update(params)


class _AppDeleteTransaction:
    def __init__(self, app_client: applications.AppClient):
        self.app_client = app_client

    def bare(self, params: applications.AppClientBareCallWithSendParams | None = None) -> Transaction:
        return self.app_client.create_transaction.bare.delete(params)


class AppCreateTransactionParams:
    def __init__(self, app_client: applications.AppClient):
        self.app_client = app_client
    @property
    def update(self) -> "_AppUpdateTransaction":
        return _AppUpdateTransaction(self.app_client)

    @property
    def delete(self) -> "_AppDeleteTransaction":
        return _AppDeleteTransaction(self.app_client)

    def clear_state(self, params: applications.AppClientBareCallWithSendParams | None = None) -> Transaction:
        return self.app_client.create_transaction.bare.clear_state(params)


class _AppUpdateSend:
    def __init__(self, app_client: applications.AppClient):
        self.app_client = app_client

    def bare(self, params: applications.AppClientBareCallWithCompilationAndSendParams | None = None) -> transactions.SendAppTransactionResult:
        return self.app_client.send.bare.update(params)


class _AppDeleteSend:
    def __init__(self, app_client: applications.AppClient):
        self.app_client = app_client

    def bare(self, params: applications.AppClientBareCallWithSendParams | None = None) -> transactions.SendAppTransactionResult:
        return self.app_client.send.bare.delete(params)


class AppSend:
    def __init__(self, app_client: applications.AppClient):
        self.app_client = app_client
    @property
    def update(self) -> "_AppUpdateSend":
        return _AppUpdateSend(self.app_client)

    @property
    def delete(self) -> "_AppDeleteSend":
        return _AppDeleteSend(self.app_client)

    def clear_state(self, params: applications.AppClientBareCallWithSendParams | None = None) -> transactions.SendAppTransactionResult[applications_abi.ABIReturn]:
        return self.app_client.send.bare.clear_state(params)


class AppState:
    """Methods to access state for the current App app"""

    def __init__(self, app_client: applications.AppClient):
        self.app_client = app_client

class AppClient:
    """Client for interacting with App smart contract"""

    @typing.overload
    def __init__(self, app_client: applications.AppClient) -> None: ...
    
    @typing.overload
    def __init__(
        self,
        *,
        algorand: protocols.AlgorandClientProtocol,
        app_id: int,
        app_name: str | None = None,
        default_sender: str | bytes | None = None,
        default_signer: TransactionSigner | None = None,
        approval_source_map: SourceMap | None = None,
        clear_source_map: SourceMap | None = None,
    ) -> None: ...

    def __init__(
        self,
        app_client: applications.AppClient | None = None,
        *,
        algorand: protocols.AlgorandClientProtocol | None = None,
        app_id: int | None = None,
        app_name: str | None = None,
        default_sender: str | bytes | None = None,
        default_signer: TransactionSigner | None = None,
        approval_source_map: SourceMap | None = None,
        clear_source_map: SourceMap | None = None,
    ) -> None:
        if app_client:
            self.app_client = app_client
        elif algorand and app_id:
            self.app_client = applications.AppClient(
                applications.AppClientParams(
                    algorand=algorand,
                    app_spec=APP_SPEC,
                    app_id=app_id,
                    app_name=app_name,
                    default_sender=default_sender,
                    default_signer=default_signer,
                    approval_source_map=approval_source_map,
                    clear_source_map=clear_source_map,
                )
            )
        else:
            raise ValueError("Either app_client or algorand and app_id must be provided")
    
        self.params = AppParams(self.app_client)
        self.create_transaction = AppCreateTransactionParams(self.app_client)
        self.send = AppSend(self.app_client)
        self.state = AppState(self.app_client)

    @staticmethod
    def from_creator_and_name(
        creator_address: str,
        app_name: str,
        algorand: protocols.AlgorandClientProtocol,
        default_sender: str | bytes | None = None,
        default_signer: TransactionSigner | None = None,
        approval_source_map: SourceMap | None = None,
        clear_source_map: SourceMap | None = None,
        ignore_cache: bool | None = None,
        app_lookup_cache: applications.AppLookup | None = None,
    ) -> "AppClient":
        return AppClient(
            applications.AppClient.from_creator_and_name(
                creator_address=creator_address,
                app_name=app_name,
                app_spec=APP_SPEC,
                algorand=algorand,
                default_sender=default_sender,
                default_signer=default_signer,
                approval_source_map=approval_source_map,
                clear_source_map=clear_source_map,
                ignore_cache=ignore_cache,
                app_lookup_cache=app_lookup_cache,
            )
        )
    
    @staticmethod
    def from_network(
        algorand: protocols.AlgorandClientProtocol,
        app_name: str | None = None,
        default_sender: str | bytes | None = None,
        default_signer: TransactionSigner | None = None,
        approval_source_map: SourceMap | None = None,
        clear_source_map: SourceMap | None = None,
    ) -> "AppClient":
        return AppClient(
            applications.AppClient.from_network(
                app_spec=APP_SPEC,
                algorand=algorand,
                app_name=app_name,
                default_sender=default_sender,
                default_signer=default_signer,
                approval_source_map=approval_source_map,
                clear_source_map=clear_source_map,
            )
        )

    @property
    def app_id(self) -> int:
        return self.app_client.app_id
    
    @property
    def app_address(self) -> str:
        return self.app_client.app_address
    
    @property
    def app_name(self) -> str:
        return self.app_client.app_name
    
    @property
    def app_spec(self) -> applications.Arc56Contract:
        return self.app_client.app_spec
    
    @property
    def algorand(self) -> protocols.AlgorandClientProtocol:
        return self.app_client.algorand

    def clone(
        self,
        app_name: str | None = None,
        default_sender: str | bytes | None = None,
        default_signer: TransactionSigner | None = None,
        approval_source_map: SourceMap | None = None,
        clear_source_map: SourceMap | None = None,
    ) -> "AppClient":
        return AppClient(
            self.app_client.clone(
                app_name=app_name,
                default_sender=default_sender,
                default_signer=default_signer,
                approval_source_map=approval_source_map,
                clear_source_map=clear_source_map,
            )
        )

    def new_group(self) -> "AppComposer":
        return AppComposer(self)

    def decode_return_value(
        self,
        method: str,
        return_value: applications_abi.ABIReturn | None
    ) -> applications_abi.ABIValue | applications_abi.ABIStruct | None:
        if return_value is None:
            return None
    
        arc56_method = self.app_spec.get_arc56_method(method)
        return return_value.get_arc56_value(arc56_method, self.app_spec.structs)


@dataclasses.dataclass(frozen=True)
class AppBareCallCreateParams(applications.AppClientCreateSchema, applications.AppClientBareCallParams, applications.BaseOnCompleteParams[typing.Literal[OnComplete.NoOpOC]]):
    """Parameters for creating App contract using bare calls"""

    def to_algokit_utils_params(self) -> applications.AppClientBareCallCreateParams:
        return applications.AppClientBareCallCreateParams(**self.__dict__)

@dataclasses.dataclass(frozen=True)
class AppBareCallUpdateParams(applications.AppClientBareCallParams):
    """Parameters for calling App contract using bare calls"""

    def to_algokit_utils_params(self) -> applications.AppClientBareCallParams:
        return applications.AppClientBareCallParams(**self.__dict__)

@dataclasses.dataclass(frozen=True)
class AppBareCallDeleteParams(applications.AppClientBareCallParams):
    """Parameters for calling App contract using bare calls"""

    def to_algokit_utils_params(self) -> applications.AppClientBareCallParams:
        return applications.AppClientBareCallParams(**self.__dict__)

class AppFactory(applications.TypedAppFactoryProtocol):
    """Factory for deploying and managing AppClient smart contracts"""

    def __init__(
        self,
        algorand: protocols.AlgorandClientProtocol,
        *,
        app_name: str | None = None,
        default_sender: str | bytes | None = None,
        default_signer: TransactionSigner | None = None,
        version: str | None = None,
        updatable: bool | None = None,
        deletable: bool | None = None,
        deploy_time_params: models.TealTemplateParams | None = None,
    ):
        self.app_factory = applications.AppFactory(
            params=applications.AppFactoryParams(
                algorand=algorand,
                app_spec=APP_SPEC,
                app_name=app_name,
                default_sender=default_sender,
                default_signer=default_signer,
                version=version,
                updatable=updatable,
                deletable=deletable,
                deploy_time_params=deploy_time_params,
            )
        )
        self.params = AppFactoryParams(self.app_factory)
        self.create_transaction = AppFactoryCreateTransaction(self.app_factory)
        self.send = AppFactorySend(self.app_factory)

    @property
    def app_name(self) -> str:
        return self.app_factory.app_name

    @property
    def app_spec(self) -> applications.Arc56Contract:
        return self.app_factory.app_spec

    @property
    def algorand(self) -> protocols.AlgorandClientProtocol:
        return self.app_factory.algorand

    def deploy(
        self,
        *,
        deploy_time_params: models.TealTemplateParams | None = None,
        on_update: applications.OnUpdate = applications.OnUpdate.Fail,
        on_schema_break: applications.OnSchemaBreak = applications.OnSchemaBreak.Fail,
        create_params: AppBareCallCreateParams | None = None,
        update_params: AppBareCallUpdateParams | None = None,
        delete_params: AppBareCallDeleteParams | None = None,
        existing_deployments: applications.AppLookup | None = None,
        ignore_cache: bool = False,
        updatable: bool | None = None,
        deletable: bool | None = None,
        app_name: str | None = None,
        max_rounds_to_wait: int | None = None,
        suppress_log: bool = False,
        populate_app_call_resources: bool = False,
    ) -> tuple[AppClient, applications.AppFactoryDeployResponse]:
        deploy_response = self.app_factory.deploy(
            deploy_time_params=deploy_time_params,
            on_update=on_update,
            on_schema_break=on_schema_break,
            create_params=create_params.to_algokit_utils_params() if create_params else None,
            update_params=update_params.to_algokit_utils_params() if update_params else None,
            delete_params=delete_params.to_algokit_utils_params() if delete_params else None,
            existing_deployments=existing_deployments,
            ignore_cache=ignore_cache,
            updatable=updatable,
            deletable=deletable,
            app_name=app_name,
            max_rounds_to_wait=max_rounds_to_wait,
            suppress_log=suppress_log,
            populate_app_call_resources=populate_app_call_resources,
        )

        return AppClient(deploy_response[0]), deploy_response[1]

    def get_app_client_by_creator_and_name(
        self,
        creator_address: str,
        app_name: str,
        default_sender: str | bytes | None = None,
        default_signer: TransactionSigner | None = None,
        ignore_cache: bool | None = None,
        app_lookup_cache: applications.AppLookup | None = None,
        approval_source_map: SourceMap | None = None,
        clear_source_map: SourceMap | None = None,
    ) -> AppClient:
        """Get an app client by creator address and name"""
        return AppClient(
            self.app_factory.get_app_client_by_creator_and_name(
                creator_address,
                app_name,
                default_sender,
                default_signer,
                ignore_cache,
                app_lookup_cache,
                approval_source_map,
                clear_source_map,
            )
        )

    def get_app_client_by_id(
        self,
        app_id: int,
        app_name: str | None = None,
        default_sender: str | bytes | None = None,
        default_signer: TransactionSigner | None = None,
        approval_source_map: SourceMap | None = None,
        clear_source_map: SourceMap | None = None,
    ) -> AppClient:
        """Get an app client by app ID"""
        return AppClient(
            self.app_factory.get_app_client_by_id(
                app_id,
                app_name,
                default_sender,
                default_signer,
                approval_source_map,
                clear_source_map,
            )
        )


class AppFactoryParams:
    """Parameters for creating transactions for App contract"""

    def __init__(self, app_factory: applications.AppFactory):
        self.app_factory = app_factory
        self.create = AppFactoryCreateParams(app_factory)
        self.deploy_update = AppFactoryUpdateParams(app_factory)
        self.deploy_delete = AppFactoryDeleteParams(app_factory)

class AppFactoryCreateParams:
    """Parameters for 'create' operations of App contract"""

    def __init__(self, app_factory: applications.AppFactory):
        self.app_factory = app_factory

    def bare(
        self,
        *,
        on_complete: (typing.Literal[
                OnComplete.NoOpOC,
                OnComplete.UpdateApplicationOC,
                OnComplete.DeleteApplicationOC,
                OnComplete.OptInOC,
                OnComplete.CloseOutOC,
            ] | None) = None,
        **kwargs
    ) -> transactions.AppCreateParams:
        """Creates an instance using a bare call"""
        return self.app_factory.params.bare.create(
            applications.AppFactoryCreateParams(on_complete=on_complete, **kwargs)
        )

class AppFactoryUpdateParams:
    """Parameters for 'update' operations of App contract"""

    def __init__(self, app_factory: applications.AppFactory):
        self.app_factory = app_factory

    def bare(
        self,
        *,
        on_complete: (typing.Literal[
                OnComplete.NoOpOC,
                OnComplete.UpdateApplicationOC,
                OnComplete.DeleteApplicationOC,
                OnComplete.OptInOC,
                OnComplete.CloseOutOC,
            ] | None) = None,
        **kwargs
    ) -> transactions.AppUpdateParams:
        """Updates an instance using a bare call"""
        return self.app_factory.params.bare.deploy_update(
            applications.AppFactoryCreateParams(on_complete=on_complete, **kwargs)
        )

class AppFactoryDeleteParams:
    """Parameters for 'delete' operations of App contract"""

    def __init__(self, app_factory: applications.AppFactory):
        self.app_factory = app_factory

    def bare(
        self,
        *,
        on_complete: (typing.Literal[
                OnComplete.NoOpOC,
                OnComplete.UpdateApplicationOC,
                OnComplete.DeleteApplicationOC,
                OnComplete.OptInOC,
                OnComplete.CloseOutOC,
            ] | None) = None,
        **kwargs
    ) -> transactions.AppDeleteParams:
        """Deletes an instance using a bare call"""
        return self.app_factory.params.bare.deploy_delete(
            applications.AppFactoryCreateParams(on_complete=on_complete, **kwargs)
        )


class AppFactoryCreateTransaction:
    """Create transactions for App contract"""

    def __init__(self, app_factory: applications.AppFactory):
        self.app_factory = app_factory
        self.create = AppFactoryCreateTransactionCreate(app_factory)

class AppFactoryCreateTransactionCreate:
    """Create new instances of App contract"""

    def __init__(self, app_factory: applications.AppFactory):
        self.app_factory = app_factory

    def bare(
        self,
        *,
        on_complete: (typing.Literal[
                OnComplete.NoOpOC,
                OnComplete.UpdateApplicationOC,
                OnComplete.DeleteApplicationOC,
                OnComplete.OptInOC,
                OnComplete.CloseOutOC,
            ] | None) = None,
        **kwargs
    ) -> Transaction:
        """Creates a new instance using a bare call"""
        return self.app_factory.create_transaction.bare.create(
            applications.AppFactoryCreateParams(on_complete=on_complete, **kwargs)
        )


class AppFactorySend:
    """Send calls to App contract"""

    def __init__(self, app_factory: applications.AppFactory):
        self.app_factory = app_factory
        self.create = AppFactorySendCreate(app_factory)


class AppFactorySendCreate:
    """Send create calls to App contract"""

    def __init__(self, app_factory: applications.AppFactory):
        self.app_factory = app_factory

    def bare(
        self,
        *,
        on_complete: (typing.Literal[
                OnComplete.NoOpOC,
                OnComplete.UpdateApplicationOC,
                OnComplete.DeleteApplicationOC,
                OnComplete.OptInOC,
                OnComplete.CloseOutOC,
            ] | None) = None,
        **kwargs
    ) -> tuple[AppClient, transactions.SendAppCreateTransactionResult]:
        """Creates a new instance using a bare call"""
        result = self.app_factory.send.bare.create(
            applications.AppFactoryCreateWithSendParams(on_complete=on_complete, **kwargs)
        )
        return AppClient(result[0]), result[1]


class _AppUpdateComposer:
    def __init__(self, composer: "AppComposer"):
        self.composer = composer


class _AppDeleteComposer:
    def __init__(self, composer: "AppComposer"):
        self.composer = composer


class AppComposer:
    """Composer for creating transaction groups for App contract calls"""

    def __init__(self, client: "AppClient"):
        self.client = client
        self._composer = client.algorand.new_group()
        self._result_mappers: list[typing.Callable[[applications_abi.ABIReturn | None], typing.Any] | None] = []

    @property
    def update(self) -> "_AppUpdateComposer":
        return _AppUpdateComposer(self)

    @property
    def delete(self) -> "_AppDeleteComposer":
        return _AppDeleteComposer(self)

    def clear_state(
        self,
        *,
        account_references: list[str] | None = None,
        app_references: list[int] | None = None,
        asset_references: list[int] | None = None,
        box_references: list[models.BoxReference | models.BoxIdentifier] | None = None,
        extra_fee: models.AlgoAmount | None = None,
        lease: bytes | None = None,
        max_fee: models.AlgoAmount | None = None,
        note: bytes | None = None,
        rekey_to: str | None = None,
        sender: str | None = None,
        signer: TransactionSigner | None = None,
        static_fee: models.AlgoAmount | None = None,
        validity_window: int | None = None,
        first_valid_round: int | None = None,
        last_valid_round: int | None = None,
    ) -> "AppComposer":
        self._composer.add_app_call(
            self.client.params.clear_state(
                applications.AppClientBareCallWithSendParams(
                    account_references=account_references,
                    app_references=app_references,
                    asset_references=asset_references,
                    box_references=box_references,
                    extra_fee=extra_fee,
                    first_valid_round=first_valid_round,
                    lease=lease,
                    max_fee=max_fee,
                    note=note,
                    rekey_to=rekey_to,
                    sender=sender,
                    signer=signer,
                    static_fee=static_fee,
                    validity_window=validity_window,
                    last_valid_round=last_valid_round,
                )
            )
        )
        return self
    
    def add_transaction(
        self, txn: Transaction, signer: TransactionSigner | None = None
    ) -> "AppComposer":
        self._composer.add_transaction(txn, signer)
        return self
    
    def composer(self) -> transactions.TransactionComposer:
        return self._composer
    
    def simulate(
        self,
        allow_more_logs: bool | None = None,
        allow_empty_signatures: bool | None = None,
        allow_unnamed_resources: bool | None = None,
        extra_opcode_budget: int | None = None,
        exec_trace_config: SimulateTraceConfig | None = None,
        simulation_round: int | None = None,
        skip_signatures: int | None = None,
    ) -> transactions.SendAtomicTransactionComposerResults:
        return self._composer.simulate(
            allow_more_logs=allow_more_logs,
            allow_empty_signatures=allow_empty_signatures,
            allow_unnamed_resources=allow_unnamed_resources,
            extra_opcode_budget=extra_opcode_budget,
            exec_trace_config=exec_trace_config,
            simulation_round=simulation_round,
            skip_signatures=skip_signatures,
        )
    
    def send(
        self,
        max_rounds_to_wait: int | None = None,
        suppress_log: bool | None = None,
        populate_app_call_resources: bool | None = None,
    ) -> transactions.SendAtomicTransactionComposerResults:
        return self._composer.send(
            max_rounds_to_wait=max_rounds_to_wait,
            suppress_log=suppress_log,
            populate_app_call_resources=populate_app_call_resources,
        )
