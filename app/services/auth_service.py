from app.auth.passwords import verify_password
from app.auth.tokens import issue_token
from app.repository.interface.member import MemberInterfaceRepo
from app.services.member_service import MemberService
from app.utilities.exceptions import AuthenticationError


class AuthService:
    def __init__(
        self,
        member_service: MemberService,
        member_repository: MemberInterfaceRepo,
        secret_key: str,
    ):
        self._member_service = member_service
        self._repo = member_repository
        self._secret_key = secret_key

    def signup(self, data: dict) -> dict:
        payload = dict(data)
        payload["role"] = "employee"
        password = payload.get("password")
        self._member_service.create(payload)
        return self.login(payload.get("email"), password)

    def login(self, email: str, password: str) -> dict:
        member = self._repo.get_by_email(email) if email else None
        if (
            not member
            or not member.get("password_hash")
            or not verify_password(password or "", member["password_hash"])
        ):
            raise AuthenticationError("invalid email or password")
        if not member.get("is_active", True):
            raise AuthenticationError("this account is deactivated")
        token = issue_token(self._secret_key, member["id"], member["role"])
        return {
            "token": token,
            "member_id": member["id"],
            "role": member["role"],
        }
