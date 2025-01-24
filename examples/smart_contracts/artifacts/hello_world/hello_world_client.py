# flake8: noqa
# fmt: off
# mypy: disable-error-code="no-any-return, no-untyped-call, misc, type-arg"
# This file was automatically generated by algokit-client-generator.
# DO NOT MODIFY IT BY HAND.
# requires: algokit-utils@^1.2.0
import base64
import dataclasses
import decimal
import typing
from abc import ABC, abstractmethod

import algokit_utils
import algosdk
from algosdk.v2client import models
from algosdk.atomic_transaction_composer import (
    AtomicTransactionComposer,
    AtomicTransactionResponse,
    SimulateAtomicTransactionResponse,
    TransactionSigner,
    TransactionWithSigner
)

_APP_SPEC_JSON = r"""{
    "hints": {
        "hello(string)string": {
            "call_config": {
                "no_op": "CALL"
            }
        },
        "hello_world_check(string)void": {
            "call_config": {
                "no_op": "CALL"
            }
        }
    },
    "source": {
        "approval": "I3ByYWdtYSB2ZXJzaW9uIDEwCiNwcmFnbWEgdHlwZXRyYWNrIGZhbHNlCgovLyBhbGdvcHkuYXJjNC5BUkM0Q29udHJhY3QuYXBwcm92YWxfcHJvZ3JhbSgpIC0+IHVpbnQ2NDoKbWFpbjoKICAgIGludGNibG9jayAxIFRNUExfVVBEQVRBQkxFIFRNUExfREVMRVRBQkxFCiAgICAvLyBleGFtcGxlcy9zbWFydF9jb250cmFjdHMvaGVsbG9fd29ybGQvY29udHJhY3QucHk6NgogICAgLy8gY2xhc3MgSGVsbG9Xb3JsZChFeGFtcGxlQVJDNENvbnRyYWN0KToKICAgIHR4biBOdW1BcHBBcmdzCiAgICBieiBtYWluX2JhcmVfcm91dGluZ0A3CiAgICBwdXNoYnl0ZXNzIDB4MDJiZWNlMTEgMHhiZjljMWVkZiAvLyBtZXRob2QgImhlbGxvKHN0cmluZylzdHJpbmciLCBtZXRob2QgImhlbGxvX3dvcmxkX2NoZWNrKHN0cmluZyl2b2lkIgogICAgdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMAogICAgbWF0Y2ggbWFpbl9oZWxsb19yb3V0ZUAzIG1haW5faGVsbG9fd29ybGRfY2hlY2tfcm91dGVANAoKbWFpbl9hZnRlcl9pZl9lbHNlQDEzOgogICAgLy8gZXhhbXBsZXMvc21hcnRfY29udHJhY3RzL2hlbGxvX3dvcmxkL2NvbnRyYWN0LnB5OjYKICAgIC8vIGNsYXNzIEhlbGxvV29ybGQoRXhhbXBsZUFSQzRDb250cmFjdCk6CiAgICBwdXNoaW50IDAgLy8gMAogICAgcmV0dXJuCgptYWluX2hlbGxvX3dvcmxkX2NoZWNrX3JvdXRlQDQ6CiAgICAvLyBleGFtcGxlcy9zbWFydF9jb250cmFjdHMvaGVsbG9fd29ybGQvY29udHJhY3QucHk6MTEKICAgIC8vIEBhcmM0LmFiaW1ldGhvZAogICAgdHhuIE9uQ29tcGxldGlvbgogICAgIQogICAgYXNzZXJ0IC8vIE9uQ29tcGxldGlvbiBpcyBub3QgTm9PcAogICAgdHhuIEFwcGxpY2F0aW9uSUQKICAgIGFzc2VydCAvLyBjYW4gb25seSBjYWxsIHdoZW4gbm90IGNyZWF0aW5nCiAgICAvLyBleGFtcGxlcy9zbWFydF9jb250cmFjdHMvaGVsbG9fd29ybGQvY29udHJhY3QucHk6NgogICAgLy8gY2xhc3MgSGVsbG9Xb3JsZChFeGFtcGxlQVJDNENvbnRyYWN0KToKICAgIHR4bmEgQXBwbGljYXRpb25BcmdzIDEKICAgIGV4dHJhY3QgMiAwCiAgICAvLyBleGFtcGxlcy9zbWFydF9jb250cmFjdHMvaGVsbG9fd29ybGQvY29udHJhY3QucHk6MTEKICAgIC8vIEBhcmM0LmFiaW1ldGhvZAogICAgY2FsbHN1YiBoZWxsb193b3JsZF9jaGVjawogICAgaW50Y18wIC8vIDEKICAgIHJldHVybgoKbWFpbl9oZWxsb19yb3V0ZUAzOgogICAgLy8gZXhhbXBsZXMvc21hcnRfY29udHJhY3RzL2hlbGxvX3dvcmxkL2NvbnRyYWN0LnB5OjcKICAgIC8vIEBhcmM0LmFiaW1ldGhvZAogICAgdHhuIE9uQ29tcGxldGlvbgogICAgIQogICAgYXNzZXJ0IC8vIE9uQ29tcGxldGlvbiBpcyBub3QgTm9PcAogICAgdHhuIEFwcGxpY2F0aW9uSUQKICAgIGFzc2VydCAvLyBjYW4gb25seSBjYWxsIHdoZW4gbm90IGNyZWF0aW5nCiAgICAvLyBleGFtcGxlcy9zbWFydF9jb250cmFjdHMvaGVsbG9fd29ybGQvY29udHJhY3QucHk6NgogICAgLy8gY2xhc3MgSGVsbG9Xb3JsZChFeGFtcGxlQVJDNENvbnRyYWN0KToKICAgIHR4bmEgQXBwbGljYXRpb25BcmdzIDEKICAgIGV4dHJhY3QgMiAwCiAgICAvLyBleGFtcGxlcy9zbWFydF9jb250cmFjdHMvaGVsbG9fd29ybGQvY29udHJhY3QucHk6NwogICAgLy8gQGFyYzQuYWJpbWV0aG9kCiAgICBjYWxsc3ViIGhlbGxvCiAgICBkdXAKICAgIGxlbgogICAgaXRvYgogICAgZXh0cmFjdCA2IDIKICAgIHN3YXAKICAgIGNvbmNhdAogICAgcHVzaGJ5dGVzIDB4MTUxZjdjNzUKICAgIHN3YXAKICAgIGNvbmNhdAogICAgbG9nCiAgICBpbnRjXzAgLy8gMQogICAgcmV0dXJuCgptYWluX2JhcmVfcm91dGluZ0A3OgogICAgLy8gZXhhbXBsZXMvc21hcnRfY29udHJhY3RzL2hlbGxvX3dvcmxkL2NvbnRyYWN0LnB5OjYKICAgIC8vIGNsYXNzIEhlbGxvV29ybGQoRXhhbXBsZUFSQzRDb250cmFjdCk6CiAgICB0eG4gT25Db21wbGV0aW9uCiAgICBzd2l0Y2ggbWFpbl9fX2FsZ29weV9kZWZhdWx0X2NyZWF0ZUA4IG1haW5fYWZ0ZXJfaWZfZWxzZUAxMyBtYWluX2FmdGVyX2lmX2Vsc2VAMTMgbWFpbl9hZnRlcl9pZl9lbHNlQDEzIG1haW5fdXBkYXRlQDkgbWFpbl9kZWxldGVAMTAKICAgIGIgbWFpbl9hZnRlcl9pZl9lbHNlQDEzCgptYWluX2RlbGV0ZUAxMDoKICAgIC8vIGV4YW1wbGVzL3NtYXJ0X2NvbnRyYWN0cy9iYXNlL2NvbnRyYWN0LnB5OjMwCiAgICAvLyBAYXJjNC5iYXJlbWV0aG9kKGFsbG93X2FjdGlvbnM9WyJEZWxldGVBcHBsaWNhdGlvbiJdKQogICAgdHhuIEFwcGxpY2F0aW9uSUQKICAgIGFzc2VydCAvLyBjYW4gb25seSBjYWxsIHdoZW4gbm90IGNyZWF0aW5nCiAgICAvLyBleGFtcGxlcy9zbWFydF9jb250cmFjdHMvYmFzZS9jb250cmFjdC5weTozMC0zMQogICAgLy8gQGFyYzQuYmFyZW1ldGhvZChhbGxvd19hY3Rpb25zPVsiRGVsZXRlQXBwbGljYXRpb24iXSkKICAgIC8vIGRlZiBkZWxldGUoc2VsZikgLT4gTm9uZToKICAgIGNhbGxzdWIgZGVsZXRlCiAgICBpbnRjXzAgLy8gMQogICAgcmV0dXJuCgptYWluX3VwZGF0ZUA5OgogICAgLy8gZXhhbXBsZXMvc21hcnRfY29udHJhY3RzL2Jhc2UvY29udHJhY3QucHk6MjMKICAgIC8vIEBhcmM0LmJhcmVtZXRob2QoYWxsb3dfYWN0aW9ucz1bIlVwZGF0ZUFwcGxpY2F0aW9uIl0pCiAgICB0eG4gQXBwbGljYXRpb25JRAogICAgYXNzZXJ0IC8vIGNhbiBvbmx5IGNhbGwgd2hlbiBub3QgY3JlYXRpbmcKICAgIC8vIGV4YW1wbGVzL3NtYXJ0X2NvbnRyYWN0cy9iYXNlL2NvbnRyYWN0LnB5OjIzLTI0CiAgICAvLyBAYXJjNC5iYXJlbWV0aG9kKGFsbG93X2FjdGlvbnM9WyJVcGRhdGVBcHBsaWNhdGlvbiJdKQogICAgLy8gZGVmIHVwZGF0ZShzZWxmKSAtPiBOb25lOgogICAgY2FsbHN1YiB1cGRhdGUKICAgIGludGNfMCAvLyAxCiAgICByZXR1cm4KCm1haW5fX19hbGdvcHlfZGVmYXVsdF9jcmVhdGVAODoKICAgIHR4biBBcHBsaWNhdGlvbklECiAgICAhCiAgICBhc3NlcnQgLy8gY2FuIG9ubHkgY2FsbCB3aGVuIGNyZWF0aW5nCiAgICBpbnRjXzAgLy8gMQogICAgcmV0dXJuCgoKLy8gZXhhbXBsZXMuc21hcnRfY29udHJhY3RzLmhlbGxvX3dvcmxkLmNvbnRyYWN0LkhlbGxvV29ybGQuaGVsbG8obmFtZTogYnl0ZXMpIC0+IGJ5dGVzOgpoZWxsbzoKICAgIC8vIGV4YW1wbGVzL3NtYXJ0X2NvbnRyYWN0cy9oZWxsb193b3JsZC9jb250cmFjdC5weTo3LTgKICAgIC8vIEBhcmM0LmFiaW1ldGhvZAogICAgLy8gZGVmIGhlbGxvKHNlbGYsIG5hbWU6IFN0cmluZykgLT4gU3RyaW5nOgogICAgcHJvdG8gMSAxCiAgICAvLyBleGFtcGxlcy9zbWFydF9jb250cmFjdHMvaGVsbG9fd29ybGQvY29udHJhY3QucHk6OQogICAgLy8gcmV0dXJuICJIZWxsbywgIiArIG5hbWUKICAgIHB1c2hieXRlcyAiSGVsbG8sICIKICAgIGZyYW1lX2RpZyAtMQogICAgY29uY2F0CiAgICByZXRzdWIKCgovLyBleGFtcGxlcy5zbWFydF9jb250cmFjdHMuaGVsbG9fd29ybGQuY29udHJhY3QuSGVsbG9Xb3JsZC5oZWxsb193b3JsZF9jaGVjayhuYW1lOiBieXRlcykgLT4gdm9pZDoKaGVsbG9fd29ybGRfY2hlY2s6CiAgICAvLyBleGFtcGxlcy9zbWFydF9jb250cmFjdHMvaGVsbG9fd29ybGQvY29udHJhY3QucHk6MTEtMTIKICAgIC8vIEBhcmM0LmFiaW1ldGhvZAogICAgLy8gZGVmIGhlbGxvX3dvcmxkX2NoZWNrKHNlbGYsIG5hbWU6IFN0cmluZykgLT4gTm9uZToKICAgIHByb3RvIDEgMAogICAgLy8gZXhhbXBsZXMvc21hcnRfY29udHJhY3RzL2hlbGxvX3dvcmxkL2NvbnRyYWN0LnB5OjEzCiAgICAvLyBhc3NlcnQgbmFtZSA9PSAiV29ybGQiCiAgICBmcmFtZV9kaWcgLTEKICAgIHB1c2hieXRlcyAiV29ybGQiCiAgICA9PQogICAgYXNzZXJ0CiAgICByZXRzdWIKCgovLyBleGFtcGxlcy5zbWFydF9jb250cmFjdHMuYmFzZS5jb250cmFjdC5JbW11dGFiaWxpdHlDb250cm9sQVJDNENvbnRyYWN0LnVwZGF0ZSgpIC0+IHZvaWQ6CnVwZGF0ZToKICAgIC8vIGV4YW1wbGVzL3NtYXJ0X2NvbnRyYWN0cy9iYXNlL2NvbnRyYWN0LnB5OjIzLTI0CiAgICAvLyBAYXJjNC5iYXJlbWV0aG9kKGFsbG93X2FjdGlvbnM9WyJVcGRhdGVBcHBsaWNhdGlvbiJdKQogICAgLy8gZGVmIHVwZGF0ZShzZWxmKSAtPiBOb25lOgogICAgcHJvdG8gMCAwCiAgICAvLyBleGFtcGxlcy9zbWFydF9jb250cmFjdHMvYmFzZS9jb250cmFjdC5weToyNQogICAgLy8gYXNzZXJ0IFRlbXBsYXRlVmFyW2Jvb2xdKFVQREFUQUJMRV9URU1QTEFURV9OQU1FKSwgIkNoZWNrIGFwcCBpcyB1cGRhdGFibGUiCiAgICBpbnRjXzEgLy8gVE1QTF9VUERBVEFCTEUKICAgIGFzc2VydCAvLyBDaGVjayBhcHAgaXMgdXBkYXRhYmxlCiAgICAvLyBleGFtcGxlcy9zbWFydF9jb250cmFjdHMvYmFzZS9jb250cmFjdC5weToyNgogICAgLy8gc2VsZi5hdXRob3JpemVfY3JlYXRvcigpCiAgICBjYWxsc3ViIGF1dGhvcml6ZV9jcmVhdG9yCiAgICByZXRzdWIKCgovLyBleGFtcGxlcy5zbWFydF9jb250cmFjdHMuYmFzZS5jb250cmFjdC5CYXNlQVJDNENvbnRyYWN0LmF1dGhvcml6ZV9jcmVhdG9yKCkgLT4gdm9pZDoKYXV0aG9yaXplX2NyZWF0b3I6CiAgICAvLyBleGFtcGxlcy9zbWFydF9jb250cmFjdHMvYmFzZS9jb250cmFjdC5weTo4LTkKICAgIC8vIEBzdWJyb3V0aW5lCiAgICAvLyBkZWYgYXV0aG9yaXplX2NyZWF0b3Ioc2VsZikgLT4gTm9uZToKICAgIHByb3RvIDAgMAogICAgLy8gZXhhbXBsZXMvc21hcnRfY29udHJhY3RzL2Jhc2UvY29udHJhY3QucHk6MTAKICAgIC8vIGFzc2VydCBUeG4uc2VuZGVyID09IEdsb2JhbC5jcmVhdG9yX2FkZHJlc3MsICJ1bmF1dGhvcml6ZWQiCiAgICB0eG4gU2VuZGVyCiAgICBnbG9iYWwgQ3JlYXRvckFkZHJlc3MKICAgID09CiAgICBhc3NlcnQgLy8gdW5hdXRob3JpemVkCiAgICByZXRzdWIKCgovLyBleGFtcGxlcy5zbWFydF9jb250cmFjdHMuYmFzZS5jb250cmFjdC5QZXJtYW5lbmNlQ29udHJvbEFSQzRDb250cmFjdC5kZWxldGUoKSAtPiB2b2lkOgpkZWxldGU6CiAgICAvLyBleGFtcGxlcy9zbWFydF9jb250cmFjdHMvYmFzZS9jb250cmFjdC5weTozMC0zMQogICAgLy8gQGFyYzQuYmFyZW1ldGhvZChhbGxvd19hY3Rpb25zPVsiRGVsZXRlQXBwbGljYXRpb24iXSkKICAgIC8vIGRlZiBkZWxldGUoc2VsZikgLT4gTm9uZToKICAgIHByb3RvIDAgMAogICAgLy8gZXhhbXBsZXMvc21hcnRfY29udHJhY3RzL2Jhc2UvY29udHJhY3QucHk6MzIKICAgIC8vIGFzc2VydCBUZW1wbGF0ZVZhcltib29sXShERUxFVEFCTEVfVEVNUExBVEVfTkFNRSksICJDaGVjayBhcHAgaXMgZGVsZXRhYmxlIgogICAgaW50Y18yIC8vIFRNUExfREVMRVRBQkxFCiAgICBhc3NlcnQgLy8gQ2hlY2sgYXBwIGlzIGRlbGV0YWJsZQogICAgLy8gZXhhbXBsZXMvc21hcnRfY29udHJhY3RzL2Jhc2UvY29udHJhY3QucHk6MzMKICAgIC8vIHNlbGYuYXV0aG9yaXplX2NyZWF0b3IoKQogICAgY2FsbHN1YiBhdXRob3JpemVfY3JlYXRvcgogICAgcmV0c3ViCg==",
        "clear": "I3ByYWdtYSB2ZXJzaW9uIDEwCiNwcmFnbWEgdHlwZXRyYWNrIGZhbHNlCgovLyBhbGdvcHkuYXJjNC5BUkM0Q29udHJhY3QuY2xlYXJfc3RhdGVfcHJvZ3JhbSgpIC0+IHVpbnQ2NDoKbWFpbjoKICAgIHB1c2hpbnQgMSAvLyAxCiAgICByZXR1cm4K"
    },
    "state": {
        "global": {
            "num_byte_slices": 0,
            "num_uints": 0
        },
        "local": {
            "num_byte_slices": 0,
            "num_uints": 0
        }
    },
    "schema": {
        "global": {
            "declared": {},
            "reserved": {}
        },
        "local": {
            "declared": {},
            "reserved": {}
        }
    },
    "contract": {
        "name": "HelloWorld",
        "methods": [
            {
                "name": "hello",
                "args": [
                    {
                        "type": "string",
                        "name": "name"
                    }
                ],
                "returns": {
                    "type": "string"
                }
            },
            {
                "name": "hello_world_check",
                "args": [
                    {
                        "type": "string",
                        "name": "name"
                    }
                ],
                "returns": {
                    "type": "void"
                }
            }
        ],
        "networks": {}
    },
    "bare_call_config": {
        "delete_application": "CALL",
        "no_op": "CREATE",
        "update_application": "CALL"
    }
}"""
APP_SPEC = algokit_utils.ApplicationSpecification.from_json(_APP_SPEC_JSON)
_TReturn = typing.TypeVar("_TReturn")


class _ArgsBase(ABC, typing.Generic[_TReturn]):
    @staticmethod
    @abstractmethod
    def method() -> str:
        ...


_TArgs = typing.TypeVar("_TArgs", bound=_ArgsBase[typing.Any])


@dataclasses.dataclass(kw_only=True)
class _TArgsHolder(typing.Generic[_TArgs]):
    args: _TArgs


def _filter_none(value: dict | typing.Any) -> dict | typing.Any:
    if isinstance(value, dict):
        return {k: _filter_none(v) for k, v in value.items() if v is not None}
    return value


def _as_dict(data: typing.Any, *, convert_all: bool = True) -> dict[str, typing.Any]:
    if data is None:
        return {}
    if not dataclasses.is_dataclass(data):
        raise TypeError(f"{data} must be a dataclass")
    if convert_all:
        result = dataclasses.asdict(data) # type: ignore[call-overload]
    else:
        result = {f.name: getattr(data, f.name) for f in dataclasses.fields(data)}
    return _filter_none(result)


def _convert_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
) -> algokit_utils.TransactionParametersDict:
    return typing.cast(algokit_utils.TransactionParametersDict, _as_dict(transaction_parameters))


def _convert_call_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
) -> algokit_utils.OnCompleteCallParametersDict:
    return typing.cast(algokit_utils.OnCompleteCallParametersDict, _as_dict(transaction_parameters))


def _convert_create_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
    on_complete: algokit_utils.OnCompleteActionName,
) -> algokit_utils.CreateCallParametersDict:
    result = typing.cast(algokit_utils.CreateCallParametersDict, _as_dict(transaction_parameters))
    on_complete_enum = on_complete.replace("_", " ").title().replace(" ", "") + "OC"
    result["on_complete"] = getattr(algosdk.transaction.OnComplete, on_complete_enum)
    return result


def _convert_deploy_args(
    deploy_args: algokit_utils.DeployCallArgs | None,
) -> algokit_utils.ABICreateCallArgsDict | None:
    if deploy_args is None:
        return None

    deploy_args_dict = typing.cast(algokit_utils.ABICreateCallArgsDict, _as_dict(deploy_args))
    if isinstance(deploy_args, _TArgsHolder):
        deploy_args_dict["args"] = _as_dict(deploy_args.args)
        deploy_args_dict["method"] = deploy_args.args.method()

    return deploy_args_dict


@dataclasses.dataclass(kw_only=True)
class HelloArgs(_ArgsBase[str]):
    name: str

    @staticmethod
    def method() -> str:
        return "hello(string)string"


@dataclasses.dataclass(kw_only=True)
class HelloWorldCheckArgs(_ArgsBase[None]):
    name: str

    @staticmethod
    def method() -> str:
        return "hello_world_check(string)void"


@dataclasses.dataclass(kw_only=True)
class SimulateOptions:
    allow_more_logs: bool = dataclasses.field(default=False)
    allow_empty_signatures: bool = dataclasses.field(default=False)
    extra_opcode_budget: int = dataclasses.field(default=0)
    exec_trace_config: models.SimulateTraceConfig | None         = dataclasses.field(default=None)


class Composer:

    def __init__(self, app_client: algokit_utils.ApplicationClient, atc: AtomicTransactionComposer):
        self.app_client = app_client
        self.atc = atc

    def build(self) -> AtomicTransactionComposer:
        return self.atc

    def simulate(self, options: SimulateOptions | None = None) -> SimulateAtomicTransactionResponse:
        request = models.SimulateRequest(
            allow_more_logs=options.allow_more_logs,
            allow_empty_signatures=options.allow_empty_signatures,
            extra_opcode_budget=options.extra_opcode_budget,
            exec_trace_config=options.exec_trace_config,
            txn_groups=[]
        ) if options else None
        result = self.atc.simulate(self.app_client.algod_client, request)
        return result

    def execute(self) -> AtomicTransactionResponse:
        return self.app_client.execute_atc(self.atc)

    def hello(
        self,
        *,
        name: str,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `hello(string)string` ABI method
        
        :param str name: The `name` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = HelloArgs(
            name=name,
        )
        self.app_client.compose_call(
            self.atc,
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return self

    def hello_world_check(
        self,
        *,
        name: str,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `hello_world_check(string)void` ABI method
        
        :param str name: The `name` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = HelloWorldCheckArgs(
            name=name,
        )
        self.app_client.compose_call(
            self.atc,
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return self

    def create_bare(
        self,
        *,
        on_complete: typing.Literal["no_op"] = "no_op",
        transaction_parameters: algokit_utils.CreateTransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to create an application using the no_op bare method
        
        :param typing.Literal[no_op] on_complete: On completion type to use
        :param algokit_utils.CreateTransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        self.app_client.compose_create(
            self.atc,
            call_abi_method=False,
            transaction_parameters=_convert_create_transaction_parameters(transaction_parameters, on_complete),
        )
        return self

    def update_bare(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a calls to the update_application bare method
        
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        self.app_client.compose_update(
            self.atc,
            call_abi_method=False,
            transaction_parameters=_convert_transaction_parameters(transaction_parameters),
        )
        return self

    def delete_bare(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a calls to the delete_application bare method
        
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        self.app_client.compose_delete(
            self.atc,
            call_abi_method=False,
            transaction_parameters=_convert_transaction_parameters(transaction_parameters),
        )
        return self

    def clear_state(
        self,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
        app_args: list[bytes] | None = None,
    ) -> "Composer":
        """Adds a call to the application with on completion set to ClearState
    
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :param list[bytes] | None app_args: (optional) Application args to pass"""
    
        self.app_client.compose_clear_state(self.atc, _convert_transaction_parameters(transaction_parameters), app_args)
        return self


class HelloWorldClient:
    """A class for interacting with the HelloWorld app providing high productivity and
    strongly typed methods to deploy and call the app"""

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
        ...

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
        ...

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
    ) -> None:
        """
        HelloWorldClient can be created with an app_id to interact with an existing application, alternatively
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
        )

    @property
    def algod_client(self) -> algosdk.v2client.algod.AlgodClient:
        return self.app_client.algod_client

    @property
    def app_id(self) -> int:
        return self.app_client.app_id

    @app_id.setter
    def app_id(self, value: int) -> None:
        self.app_client.app_id = value

    @property
    def app_address(self) -> str:
        return self.app_client.app_address

    @property
    def sender(self) -> str | None:
        return self.app_client.sender

    @sender.setter
    def sender(self, value: str) -> None:
        self.app_client.sender = value

    @property
    def signer(self) -> TransactionSigner | None:
        return self.app_client.signer

    @signer.setter
    def signer(self, value: TransactionSigner) -> None:
        self.app_client.signer = value

    @property
    def suggested_params(self) -> algosdk.transaction.SuggestedParams | None:
        return self.app_client.suggested_params

    @suggested_params.setter
    def suggested_params(self, value: algosdk.transaction.SuggestedParams | None) -> None:
        self.app_client.suggested_params = value

    def hello(
        self,
        *,
        name: str,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[str]:
        """Calls `hello(string)string` ABI method
        
        :param str name: The `name` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[str]: The result of the transaction"""

        args = HelloArgs(
            name=name,
        )
        result = self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return result

    def hello_world_check(
        self,
        *,
        name: str,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[None]:
        """Calls `hello_world_check(string)void` ABI method
        
        :param str name: The `name` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[None]: The result of the transaction"""

        args = HelloWorldCheckArgs(
            name=name,
        )
        result = self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return result

    def create_bare(
        self,
        *,
        on_complete: typing.Literal["no_op"] = "no_op",
        transaction_parameters: algokit_utils.CreateTransactionParameters | None = None,
    ) -> algokit_utils.TransactionResponse:
        """Creates an application using the no_op bare method
        
        :param typing.Literal[no_op] on_complete: On completion type to use
        :param algokit_utils.CreateTransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.TransactionResponse: The result of the transaction"""

        result = self.app_client.create(
            call_abi_method=False,
            transaction_parameters=_convert_create_transaction_parameters(transaction_parameters, on_complete),
        )
        return result

    def update_bare(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.TransactionResponse:
        """Calls the update_application bare method
        
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.TransactionResponse: The result of the transaction"""

        result = self.app_client.update(
            call_abi_method=False,
            transaction_parameters=_convert_transaction_parameters(transaction_parameters),
        )
        return result

    def delete_bare(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.TransactionResponse:
        """Calls the delete_application bare method
        
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.TransactionResponse: The result of the transaction"""

        result = self.app_client.delete(
            call_abi_method=False,
            transaction_parameters=_convert_transaction_parameters(transaction_parameters),
        )
        return result

    def clear_state(
        self,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
        app_args: list[bytes] | None = None,
    ) -> algokit_utils.TransactionResponse:
        """Calls the application with on completion set to ClearState
    
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :param list[bytes] | None app_args: (optional) Application args to pass
        :returns algokit_utils.TransactionResponse: The result of the transaction"""
    
        return self.app_client.clear_state(_convert_transaction_parameters(transaction_parameters), app_args)

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
        template_values: algokit_utils.TemplateValueMapping | None = None,
        create_args: algokit_utils.DeployCallArgs | None = None,
        update_args: algokit_utils.DeployCallArgs | None = None,
        delete_args: algokit_utils.DeployCallArgs | None = None,
    ) -> algokit_utils.DeployResponse:
        """Deploy an application and update client to reference it.
        
        Idempotently deploy (create, update/delete if changed) an app against the given name via the given creator
        account, including deploy-time template placeholder substitutions.
        To understand the architecture decisions behind this functionality please see
        <https://github.com/algorandfoundation/algokit-cli/blob/main/docs/architecture-decisions/2023-01-12_smart-contract-deployment.md>
        
        ```{note}
        If there is a breaking state schema change to an existing app (and `on_schema_break` is set to
        'ReplaceApp' the existing app will be deleted and re-created.
        ```
        
        ```{note}
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
        :param algokit_utils.DeployCallArgs | None create_args: Arguments used when creating an application
        :param algokit_utils.DeployCallArgs | None update_args: Arguments used when updating an application
        :param algokit_utils.DeployCallArgs | None delete_args: Arguments used when deleting an application
        :return DeployResponse: details action taken and relevant transactions
        :raises DeploymentError: If the deployment failed"""

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
        )

    def compose(self, atc: AtomicTransactionComposer | None = None) -> Composer:
        return Composer(self.app_client, atc or AtomicTransactionComposer())
