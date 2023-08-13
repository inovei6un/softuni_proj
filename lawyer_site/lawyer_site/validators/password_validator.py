from django.core.exceptions import ValidationError

COMMON_PASSWORDS = ["123456",
                    "password",
                    "123456789",
                    "12345",
                    "12345678",
                    "qwerty",
                    "1234567",
                    "111111",
                    "1234567890",
                    "123123",
                    "abc123",
                    "1234",
                    "password1",
                    "iloveyou",
                    "1q2w3e4r",
                    "000000",
                    "qwerty123",
                    "zaq12wsx",
                    "dragon",
                    "sunshine",
                    "princess",
                    "letmein",
                    "654321",
                    "monkey",
                    "27653",
                    "1qaz2wsx",
                    "123321",
                    "qwertyuiop",
                    "superman",
                    "asdfghjkl",
                    ]


def validate_common_password(value):
    if value.lower() in COMMON_PASSWORDS:
        raise ValidationError("Паролата е твърде лесна!", code="password_too_common")

    if value.isalpha():
        raise ValidationError("Паролата не може да съдържа само букви!", code="password_only_letters")

    if value.isdigit():
        raise ValidationError("Паролата не може да съдържа само числа!", code="password_only_numbers")

    if value.islower():
        raise ValidationError("Паролата не може да съдържа само малки букви!", code="password_only_lowercase")

    if value.isupper():
        raise ValidationError("Паролата не може да съдържа само главни букви!", code="password_only_uppercase")
