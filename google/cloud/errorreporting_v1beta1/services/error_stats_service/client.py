# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from collections import OrderedDict
import os
import re
from typing import (
    Dict,
    Callable,
    Mapping,
    MutableMapping,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
)
import warnings

from google.cloud.errorreporting_v1beta1 import gapic_version as package_version

from google.api_core import client_options as client_options_lib
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.oauth2 import service_account  # type: ignore

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

from google.cloud.errorreporting_v1beta1.services.error_stats_service import pagers
from google.cloud.errorreporting_v1beta1.types import common
from google.cloud.errorreporting_v1beta1.types import error_stats_service
from .transports.base import ErrorStatsServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import ErrorStatsServiceGrpcTransport
from .transports.grpc_asyncio import ErrorStatsServiceGrpcAsyncIOTransport
from .transports.rest import ErrorStatsServiceRestTransport


class ErrorStatsServiceClientMeta(type):
    """Metaclass for the ErrorStatsService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[ErrorStatsServiceTransport]]
    _transport_registry["grpc"] = ErrorStatsServiceGrpcTransport
    _transport_registry["grpc_asyncio"] = ErrorStatsServiceGrpcAsyncIOTransport
    _transport_registry["rest"] = ErrorStatsServiceRestTransport

    def get_transport_class(
        cls,
        label: Optional[str] = None,
    ) -> Type[ErrorStatsServiceTransport]:
        """Returns an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class ErrorStatsServiceClient(metaclass=ErrorStatsServiceClientMeta):
    """An API for retrieving and managing error statistics as well
    as data for individual events.
    """

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Converts api endpoint to mTLS endpoint.

        Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
        "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
        Args:
            api_endpoint (Optional[str]): the api endpoint to convert.
        Returns:
            str: converted mTLS api endpoint.
        """
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    # Note: DEFAULT_ENDPOINT is deprecated. Use _DEFAULT_ENDPOINT_TEMPLATE instead.
    DEFAULT_ENDPOINT = "clouderrorreporting.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    _DEFAULT_ENDPOINT_TEMPLATE = "clouderrorreporting.{UNIVERSE_DOMAIN}"
    _DEFAULT_UNIVERSE = "googleapis.com"

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            ErrorStatsServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_info(info)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            ErrorStatsServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> ErrorStatsServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            ErrorStatsServiceTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def error_group_path(
        project: str,
        group: str,
    ) -> str:
        """Returns a fully-qualified error_group string."""
        return "projects/{project}/groups/{group}".format(
            project=project,
            group=group,
        )

    @staticmethod
    def parse_error_group_path(path: str) -> Dict[str, str]:
        """Parses a error_group path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/groups/(?P<group>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_billing_account_path(
        billing_account: str,
    ) -> str:
        """Returns a fully-qualified billing_account string."""
        return "billingAccounts/{billing_account}".format(
            billing_account=billing_account,
        )

    @staticmethod
    def parse_common_billing_account_path(path: str) -> Dict[str, str]:
        """Parse a billing_account path into its component segments."""
        m = re.match(r"^billingAccounts/(?P<billing_account>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_folder_path(
        folder: str,
    ) -> str:
        """Returns a fully-qualified folder string."""
        return "folders/{folder}".format(
            folder=folder,
        )

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str, str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(
        organization: str,
    ) -> str:
        """Returns a fully-qualified organization string."""
        return "organizations/{organization}".format(
            organization=organization,
        )

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str, str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(
        project: str,
    ) -> str:
        """Returns a fully-qualified project string."""
        return "projects/{project}".format(
            project=project,
        )

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str, str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(
        project: str,
        location: str,
    ) -> str:
        """Returns a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(
            project=project,
            location=location,
        )

    @staticmethod
    def parse_common_location_path(path: str) -> Dict[str, str]:
        """Parse a location path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)$", path)
        return m.groupdict() if m else {}

    @classmethod
    def get_mtls_endpoint_and_cert_source(
        cls, client_options: Optional[client_options_lib.ClientOptions] = None
    ):
        """Deprecated. Return the API endpoint and client cert source for mutual TLS.

        The client cert source is determined in the following order:
        (1) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is not "true", the
        client cert source is None.
        (2) if `client_options.client_cert_source` is provided, use the provided one; if the
        default client cert source exists, use the default one; otherwise the client cert
        source is None.

        The API endpoint is determined in the following order:
        (1) if `client_options.api_endpoint` if provided, use the provided one.
        (2) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is "always", use the
        default mTLS endpoint; if the environment variable is "never", use the default API
        endpoint; otherwise if client cert source exists, use the default mTLS endpoint, otherwise
        use the default API endpoint.

        More details can be found at https://google.aip.dev/auth/4114.

        Args:
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. Only the `api_endpoint` and `client_cert_source` properties may be used
                in this method.

        Returns:
            Tuple[str, Callable[[], Tuple[bytes, bytes]]]: returns the API endpoint and the
                client cert source to use.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If any errors happen.
        """

        warnings.warn(
            "get_mtls_endpoint_and_cert_source is deprecated. Use the api_endpoint property instead.",
            DeprecationWarning,
        )
        if client_options is None:
            client_options = client_options_lib.ClientOptions()
        use_client_cert = os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false")
        use_mtls_endpoint = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
        if use_client_cert not in ("true", "false"):
            raise ValueError(
                "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
            )
        if use_mtls_endpoint not in ("auto", "never", "always"):
            raise MutualTLSChannelError(
                "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
            )

        # Figure out the client cert source to use.
        client_cert_source = None
        if use_client_cert == "true":
            if client_options.client_cert_source:
                client_cert_source = client_options.client_cert_source
            elif mtls.has_default_client_cert_source():
                client_cert_source = mtls.default_client_cert_source()

        # Figure out which api endpoint to use.
        if client_options.api_endpoint is not None:
            api_endpoint = client_options.api_endpoint
        elif use_mtls_endpoint == "always" or (
            use_mtls_endpoint == "auto" and client_cert_source
        ):
            api_endpoint = cls.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = cls.DEFAULT_ENDPOINT

        return api_endpoint, client_cert_source

    @staticmethod
    def _read_environment_variables():
        """Returns the environment variables used by the client.

        Returns:
            Tuple[bool, str, str]: returns the GOOGLE_API_USE_CLIENT_CERTIFICATE,
            GOOGLE_API_USE_MTLS_ENDPOINT, and GOOGLE_CLOUD_UNIVERSE_DOMAIN environment variables.

        Raises:
            ValueError: If GOOGLE_API_USE_CLIENT_CERTIFICATE is not
                any of ["true", "false"].
            google.auth.exceptions.MutualTLSChannelError: If GOOGLE_API_USE_MTLS_ENDPOINT
                is not any of ["auto", "never", "always"].
        """
        use_client_cert = os.getenv(
            "GOOGLE_API_USE_CLIENT_CERTIFICATE", "false"
        ).lower()
        use_mtls_endpoint = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto").lower()
        universe_domain_env = os.getenv("GOOGLE_CLOUD_UNIVERSE_DOMAIN")
        if use_client_cert not in ("true", "false"):
            raise ValueError(
                "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
            )
        if use_mtls_endpoint not in ("auto", "never", "always"):
            raise MutualTLSChannelError(
                "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
            )
        return use_client_cert == "true", use_mtls_endpoint, universe_domain_env

    @staticmethod
    def _get_client_cert_source(provided_cert_source, use_cert_flag):
        """Return the client cert source to be used by the client.

        Args:
            provided_cert_source (bytes): The client certificate source provided.
            use_cert_flag (bool): A flag indicating whether to use the client certificate.

        Returns:
            bytes or None: The client cert source to be used by the client.
        """
        client_cert_source = None
        if use_cert_flag:
            if provided_cert_source:
                client_cert_source = provided_cert_source
            elif mtls.has_default_client_cert_source():
                client_cert_source = mtls.default_client_cert_source()
        return client_cert_source

    @staticmethod
    def _get_api_endpoint(
        api_override, client_cert_source, universe_domain, use_mtls_endpoint
    ):
        """Return the API endpoint used by the client.

        Args:
            api_override (str): The API endpoint override. If specified, this is always
                the return value of this function and the other arguments are not used.
            client_cert_source (bytes): The client certificate source used by the client.
            universe_domain (str): The universe domain used by the client.
            use_mtls_endpoint (str): How to use the mTLS endpoint, which depends also on the other parameters.
                Possible values are "always", "auto", or "never".

        Returns:
            str: The API endpoint to be used by the client.
        """
        if api_override is not None:
            api_endpoint = api_override
        elif use_mtls_endpoint == "always" or (
            use_mtls_endpoint == "auto" and client_cert_source
        ):
            _default_universe = ErrorStatsServiceClient._DEFAULT_UNIVERSE
            if universe_domain != _default_universe:
                raise MutualTLSChannelError(
                    f"mTLS is not supported in any universe other than {_default_universe}."
                )
            api_endpoint = ErrorStatsServiceClient.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = ErrorStatsServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=universe_domain
            )
        return api_endpoint

    @staticmethod
    def _get_universe_domain(
        client_universe_domain: Optional[str], universe_domain_env: Optional[str]
    ) -> str:
        """Return the universe domain used by the client.

        Args:
            client_universe_domain (Optional[str]): The universe domain configured via the client options.
            universe_domain_env (Optional[str]): The universe domain configured via the "GOOGLE_CLOUD_UNIVERSE_DOMAIN" environment variable.

        Returns:
            str: The universe domain to be used by the client.

        Raises:
            ValueError: If the universe domain is an empty string.
        """
        universe_domain = ErrorStatsServiceClient._DEFAULT_UNIVERSE
        if client_universe_domain is not None:
            universe_domain = client_universe_domain
        elif universe_domain_env is not None:
            universe_domain = universe_domain_env
        if len(universe_domain.strip()) == 0:
            raise ValueError("Universe Domain cannot be an empty string.")
        return universe_domain

    @staticmethod
    def _compare_universes(
        client_universe: str, credentials: ga_credentials.Credentials
    ) -> bool:
        """Returns True iff the universe domains used by the client and credentials match.

        Args:
            client_universe (str): The universe domain configured via the client options.
            credentials (ga_credentials.Credentials): The credentials being used in the client.

        Returns:
            bool: True iff client_universe matches the universe in credentials.

        Raises:
            ValueError: when client_universe does not match the universe in credentials.
        """

        default_universe = ErrorStatsServiceClient._DEFAULT_UNIVERSE
        credentials_universe = getattr(credentials, "universe_domain", default_universe)

        if client_universe != credentials_universe:
            raise ValueError(
                "The configured universe domain "
                f"({client_universe}) does not match the universe domain "
                f"found in the credentials ({credentials_universe}). "
                "If you haven't configured the universe domain explicitly, "
                f"`{default_universe}` is the default."
            )
        return True

    def _validate_universe_domain(self):
        """Validates client's and credentials' universe domains are consistent.

        Returns:
            bool: True iff the configured universe domain is valid.

        Raises:
            ValueError: If the configured universe domain is not valid.
        """
        self._is_universe_domain_valid = (
            self._is_universe_domain_valid
            or ErrorStatsServiceClient._compare_universes(
                self.universe_domain, self.transport._credentials
            )
        )
        return self._is_universe_domain_valid

    @property
    def api_endpoint(self):
        """Return the API endpoint used by the client instance.

        Returns:
            str: The API endpoint used by the client instance.
        """
        return self._api_endpoint

    @property
    def universe_domain(self) -> str:
        """Return the universe domain used by the client instance.

        Returns:
            str: The universe domain used by the client instance.
        """
        return self._universe_domain

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Optional[
            Union[
                str,
                ErrorStatsServiceTransport,
                Callable[..., ErrorStatsServiceTransport],
            ]
        ] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the error stats service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Optional[Union[str,ErrorStatsServiceTransport,Callable[..., ErrorStatsServiceTransport]]]):
                The transport to use, or a Callable that constructs and returns a new transport.
                If a Callable is given, it will be called with the same set of initialization
                arguments as used in the ErrorStatsServiceTransport constructor.
                If set to None, a transport is chosen automatically.
            client_options (Optional[Union[google.api_core.client_options.ClientOptions, dict]]):
                Custom options for the client.

                1. The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client when ``transport`` is
                not explicitly provided. Only if this property is not set and
                ``transport`` was not explicitly provided, the endpoint is
                determined by the GOOGLE_API_USE_MTLS_ENDPOINT environment
                variable, which have one of the following values:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto-switch to the
                default mTLS endpoint if client certificate is present; this is
                the default value).

                2. If the GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide a client certificate for mTLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

                3. The ``universe_domain`` property can be used to override the
                default "googleapis.com" universe. Note that the ``api_endpoint``
                property still takes precedence; and ``universe_domain`` is
                currently not supported for mTLS.

            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client_options = client_options
        if isinstance(self._client_options, dict):
            self._client_options = client_options_lib.from_dict(self._client_options)
        if self._client_options is None:
            self._client_options = client_options_lib.ClientOptions()
        self._client_options = cast(
            client_options_lib.ClientOptions, self._client_options
        )

        universe_domain_opt = getattr(self._client_options, "universe_domain", None)

        (
            self._use_client_cert,
            self._use_mtls_endpoint,
            self._universe_domain_env,
        ) = ErrorStatsServiceClient._read_environment_variables()
        self._client_cert_source = ErrorStatsServiceClient._get_client_cert_source(
            self._client_options.client_cert_source, self._use_client_cert
        )
        self._universe_domain = ErrorStatsServiceClient._get_universe_domain(
            universe_domain_opt, self._universe_domain_env
        )
        self._api_endpoint = None  # updated below, depending on `transport`

        # Initialize the universe domain validation.
        self._is_universe_domain_valid = False

        api_key_value = getattr(self._client_options, "api_key", None)
        if api_key_value and credentials:
            raise ValueError(
                "client_options.api_key and credentials are mutually exclusive"
            )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        transport_provided = isinstance(transport, ErrorStatsServiceTransport)
        if transport_provided:
            # transport is a ErrorStatsServiceTransport instance.
            if credentials or self._client_options.credentials_file or api_key_value:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if self._client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, provide its scopes "
                    "directly."
                )
            self._transport = cast(ErrorStatsServiceTransport, transport)
            self._api_endpoint = self._transport.host

        self._api_endpoint = (
            self._api_endpoint
            or ErrorStatsServiceClient._get_api_endpoint(
                self._client_options.api_endpoint,
                self._client_cert_source,
                self._universe_domain,
                self._use_mtls_endpoint,
            )
        )

        if not transport_provided:
            import google.auth._default  # type: ignore

            if api_key_value and hasattr(
                google.auth._default, "get_api_key_credentials"
            ):
                credentials = google.auth._default.get_api_key_credentials(
                    api_key_value
                )

            transport_init: Union[
                Type[ErrorStatsServiceTransport],
                Callable[..., ErrorStatsServiceTransport],
            ] = (
                type(self).get_transport_class(transport)
                if isinstance(transport, str) or transport is None
                else cast(Callable[..., ErrorStatsServiceTransport], transport)
            )
            # initialize with the provided callable or the passed in class
            self._transport = transport_init(
                credentials=credentials,
                credentials_file=self._client_options.credentials_file,
                host=self._api_endpoint,
                scopes=self._client_options.scopes,
                client_cert_source_for_mtls=self._client_cert_source,
                quota_project_id=self._client_options.quota_project_id,
                client_info=client_info,
                always_use_jwt_access=True,
                api_audience=self._client_options.api_audience,
            )

    def list_group_stats(
        self,
        request: Optional[
            Union[error_stats_service.ListGroupStatsRequest, dict]
        ] = None,
        *,
        project_name: Optional[str] = None,
        time_range: Optional[error_stats_service.QueryTimeRange] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListGroupStatsPager:
        r"""Lists the specified groups.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import errorreporting_v1beta1

            def sample_list_group_stats():
                # Create a client
                client = errorreporting_v1beta1.ErrorStatsServiceClient()

                # Initialize request argument(s)
                request = errorreporting_v1beta1.ListGroupStatsRequest(
                    project_name="project_name_value",
                )

                # Make the request
                page_result = client.list_group_stats(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.errorreporting_v1beta1.types.ListGroupStatsRequest, dict]):
                The request object. Specifies a set of ``ErrorGroupStats`` to return.
            project_name (str):
                Required. The resource name of the Google Cloud Platform
                project. Written as ``projects/{projectID}`` or
                ``projects/{projectNumber}``, where ``{projectID}`` and
                ``{projectNumber}`` can be found in the `Google Cloud
                console <https://support.google.com/cloud/answer/6158840>`__.
                It may also include a location, such as
                ``projects/{projectID}/locations/{location}`` where
                ``{location}`` is a cloud region.

                Examples: ``projects/my-project-123``,
                ``projects/5551234``,
                ``projects/my-project-123/locations/us-central1``,
                ``projects/5551234/locations/us-central1``.

                For a list of supported locations, see `Supported
                Regions <https://cloud.google.com/logging/docs/region-support>`__.
                ``global`` is the default when unspecified. Use ``-`` as
                a wildcard to request group stats from all regions.

                This corresponds to the ``project_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            time_range (google.cloud.errorreporting_v1beta1.types.QueryTimeRange):
                Optional. List data for the given time range. If not
                set, a default time range is used. The field
                [time_range_begin]
                [google.devtools.clouderrorreporting.v1beta1.ListGroupStatsResponse.time_range_begin]
                in the response will specify the beginning of this time
                range. Only [ErrorGroupStats]
                [google.devtools.clouderrorreporting.v1beta1.ErrorGroupStats]
                with a non-zero count in the given time range are
                returned, unless the request contains an explicit
                [group_id]
                [google.devtools.clouderrorreporting.v1beta1.ListGroupStatsRequest.group_id]
                list. If a [group_id]
                [google.devtools.clouderrorreporting.v1beta1.ListGroupStatsRequest.group_id]
                list is given, also [ErrorGroupStats]
                [google.devtools.clouderrorreporting.v1beta1.ErrorGroupStats]
                with zero occurrences are returned.

                This corresponds to the ``time_range`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.errorreporting_v1beta1.services.error_stats_service.pagers.ListGroupStatsPager:
                Contains a set of requested error
                group stats.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_name, time_range])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, error_stats_service.ListGroupStatsRequest):
            request = error_stats_service.ListGroupStatsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_name is not None:
                request.project_name = project_name
            if time_range is not None:
                request.time_range = time_range

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_group_stats]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("project_name", request.project_name),)
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListGroupStatsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_events(
        self,
        request: Optional[Union[error_stats_service.ListEventsRequest, dict]] = None,
        *,
        project_name: Optional[str] = None,
        group_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListEventsPager:
        r"""Lists the specified events.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import errorreporting_v1beta1

            def sample_list_events():
                # Create a client
                client = errorreporting_v1beta1.ErrorStatsServiceClient()

                # Initialize request argument(s)
                request = errorreporting_v1beta1.ListEventsRequest(
                    project_name="project_name_value",
                    group_id="group_id_value",
                )

                # Make the request
                page_result = client.list_events(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.errorreporting_v1beta1.types.ListEventsRequest, dict]):
                The request object. Specifies a set of error events to
                return.
            project_name (str):
                Required. The resource name of the Google Cloud Platform
                project. Written as ``projects/{projectID}`` or
                ``projects/{projectID}/locations/{location}``, where
                ``{projectID}`` is the `Google Cloud Platform project
                ID <https://support.google.com/cloud/answer/6158840>`__
                and ``{location}`` is a Cloud region.

                Examples: ``projects/my-project-123``,
                ``projects/my-project-123/locations/global``.

                For a list of supported locations, see `Supported
                Regions <https://cloud.google.com/logging/docs/region-support>`__.
                ``global`` is the default when unspecified.

                This corresponds to the ``project_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            group_id (str):
                Required. The group for which events shall be returned.
                The ``group_id`` is a unique identifier for a particular
                error group. The identifier is derived from key parts of
                the error-log content and is treated as Service Data.
                For information about how Service Data is handled, see
                `Google Cloud Privacy
                Notice <https://cloud.google.com/terms/cloud-privacy-notice>`__.

                This corresponds to the ``group_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.errorreporting_v1beta1.services.error_stats_service.pagers.ListEventsPager:
                Contains a set of requested error
                events.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_name, group_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, error_stats_service.ListEventsRequest):
            request = error_stats_service.ListEventsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_name is not None:
                request.project_name = project_name
            if group_id is not None:
                request.group_id = group_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_events]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("project_name", request.project_name),)
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListEventsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_events(
        self,
        request: Optional[Union[error_stats_service.DeleteEventsRequest, dict]] = None,
        *,
        project_name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> error_stats_service.DeleteEventsResponse:
        r"""Deletes all error events of a given project.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import errorreporting_v1beta1

            def sample_delete_events():
                # Create a client
                client = errorreporting_v1beta1.ErrorStatsServiceClient()

                # Initialize request argument(s)
                request = errorreporting_v1beta1.DeleteEventsRequest(
                    project_name="project_name_value",
                )

                # Make the request
                response = client.delete_events(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.errorreporting_v1beta1.types.DeleteEventsRequest, dict]):
                The request object. Deletes all events in the project.
            project_name (str):
                Required. The resource name of the Google Cloud Platform
                project. Written as ``projects/{projectID}`` or
                ``projects/{projectID}/locations/{location}``, where
                ``{projectID}`` is the `Google Cloud Platform project
                ID <https://support.google.com/cloud/answer/6158840>`__
                and ``{location}`` is a Cloud region.

                Examples: ``projects/my-project-123``,
                ``projects/my-project-123/locations/global``.

                For a list of supported locations, see `Supported
                Regions <https://cloud.google.com/logging/docs/region-support>`__.
                ``global`` is the default when unspecified.

                This corresponds to the ``project_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.errorreporting_v1beta1.types.DeleteEventsResponse:
                Response message for deleting error
                events.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, error_stats_service.DeleteEventsRequest):
            request = error_stats_service.DeleteEventsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_name is not None:
                request.project_name = project_name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_events]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("project_name", request.project_name),)
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def __enter__(self) -> "ErrorStatsServiceClient":
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("ErrorStatsServiceClient",)
