def dapp_secret_(secret):
    a = 0
    b = 0
    for d in secret:
        if a == 0:
            dapp_secret = "b'\\x"
        if b == 2:
            dapp_secret_ = "\\x"
            dapp_secret = dapp_secret + dapp_secret_
            b = 0
        dapp_secret = dapp_secret + d
        a += 1
        b += 1
    dapp_secret = dapp_secret + "'"
    dapp_secret = dapp_secret.replace("&", "")
    # dapp_secret = eval(dapp_secret)
    return dapp_secret
