from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

TOKEN_MAX_AGE_SECONDS = 60 * 60 * 8


def make_serializer(secret_key: str) -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(secret_key, salt="hrms-auth")


def issue_token(secret_key: str, member_id: str, role: str) -> str:
    return make_serializer(secret_key).dumps({"member_id": member_id, "role": role})


def verify_token(secret_key: str, token: str) -> dict:
    try:
        return make_serializer(secret_key).loads(token, max_age=TOKEN_MAX_AGE_SECONDS)
    except SignatureExpired:
        raise ValueError("token has expired")
    except BadSignature:
        raise ValueError("token is invalid")
        