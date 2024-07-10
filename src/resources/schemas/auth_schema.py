auth_request_attribute = {
    'phone_number': {
        'type': str,
        'required': True,
        'help': 'Mobile Phone Number is required'
    },
}

magic_link_generate_attribute = {
    'phone_number': {
        'type': str,
        'required': True,
        'help': 'Mobile Phone Number is required'
    },
    'magic_link_entry_point': {
        'type': str,
        'required': False,
        'help': 'Entry Point for the Magic Link'
    }
}

sign_in_attribute = {
    'phone_number': {
        'type': str,
        'required': True,
        'help': 'Mobile Phone Number is required'
    },
    'otp': {
        'type': str,
        'required': False,
        'help': 'One-Time Password'
    },
    'entry_point': {
        'type': str,
        'required': False,
        'default': '/',
        'help': 'Entry Point for the sign-in'
    },
    'bypass_otp': {
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