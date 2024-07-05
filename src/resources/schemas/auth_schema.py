auth_request_attribute = {
    'phoneNumber': {
        'type': str,
        'required': True,
        'help': 'Mobile Phone Number is required'
    },
}

magic_link_generate_attribute = {
    'phoneNumber': {
        'type': str,
        'required': True,
        'help': 'Mobile Phone Number is required'
    },
    'magicLinkEntryPoint': {
        'type': str,
        'required': False,
        'help': 'Entry Point for the Magic Link'
    }
}

sign_in_attribute = {
    'phoneNumber': {
        'type': str,
        'required': True,
        'help': 'Mobile Phone Number is required'
    },
    'otp': {
        'type': str,
        'required': False,
        'help': 'One-Time Password'
    },
    'entryPoint': {
        'type': str,
        'required': False,
        'default': '/',
        'help': 'Entry Point for the sign-in'
    },
    'bypassOtp': {
        'type': bool,
        'required': False,
        'default': False,
        'help': 'Bypass OTP verification'
    },
    'email': {
        'type': str,
        'required': False,
        'help': 'Email Address for Admin Sign-In'
    },
    'password': {
        'type': str,
        'required': False,
        'help': 'Password for Admin Sign-In'
    }
}