import re


def password_validation(password):
    regex = r"^(?!.*(.)\1\1)(?!.*(012|123|234|345|456|567|678|789|987|876|765|654|543|321|210))(?!.*(ABC|BCD|CDE|DEF|EFG|FGH|GHI|HIJ|IJK|JKL|KLM|LMN|MNO|NOP|OPQ|PQR|QRS|RST|STU|TUV|UVW|VWX|WXY|XYZ|ZYX|YXW|XWV|WVU|VUT|UTS|TSR|SRQ|RQP|QPO|PON|ONM|NML|MLK|LKJ|KJI|JIH|IHG|HGF|GFE|FED|EDC|DCB|CBA))(?!.*(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz|zyx|yxw|xwv|wvu|vut|uts|tsr|srq|rqp|qpo|pon|onm|nml|mlk|lkj|kji|jih|ihg|hgf|gfe|fed|edc|dcb|cba))(?=.*[A-Za-z])(?=.*\d)(?=.*[%@#!+\$])[A-Za-z\d%@#!+\$]{6,16}$"  # noqa: E501
    valida = re.match(regex, password)
    if valida:
        return valida
