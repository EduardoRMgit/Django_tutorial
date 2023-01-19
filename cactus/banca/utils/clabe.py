import sys

from django.conf import settings


PREFIJO_CUENTA_INGUZ = settings.PREFIJO_CUENTA_INGUZ


def es_cuenta_inguz(clabe):

    # Validar construcción de la clabe
    return isinstance(clabe, str) and clabe[:10] == PREFIJO_CUENTA_INGUZ


def calculateCheckerDigit(claveSpei, plaza, accountNumber):
    if len(accountNumber) == 11:
        pass
    else:
        print('Please check the account number length')
        sys.exit()

    last_three_SPEI_numbers = claveSpei[-3:]

    if len(last_three_SPEI_numbers) == 3:
        pass
    else:
        print("Please check the SPEI participant key identifier")
        sys.exit()

    initial_clabe = (last_three_SPEI_numbers+plaza+accountNumber)

    print("Initial CLABE is {}".format(initial_clabe))

    ponderacion = [3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7]

    pre_checker_digit = []

    # Step 1: Multiply each digit in the initial_clabe per
    # each positional weighing factor
    for i in range(0, 17):
        print(i)
        x = ponderacion[i]
        y = int(initial_clabe[i])
        step_one = x*y
        step_one = str(step_one)
        print('step_one sin modulo 10 = {}'.format(step_one))

        # Step 2: take mod10 from step 1 result
        if len(step_one) == 2:
            step_one = step_one[1]
            step_two = int(step_one)
        else:
            pass
        step_two = int(step_one)
        pre_checker_digit.append(step_two)
        print('step_two es {}'.format(step_two))

    print('Resultado del append = {}'.format(pre_checker_digit))

    # Step 3: Sum all the results from step 2
    step_three = sum(pre_checker_digit)
    print('step_three es {}'.format(step_three))

    # Step 4: take mod10 from the sum
    step_three = str(step_three)
    if len(step_three) == 2:
        step_four = step_three[1]
    else:
        step_four = step_three
    step_four = int(step_four)

    # Step 5: Subtract 10 - step four
    step_five = 10-step_four
    print('step_five es {}'.format(step_five))

    # Step 6: Take mod10 from step 5
    step_five = str(step_five)
    if len(step_five) == 2:
        step_six = step_five[1]
    else:
        step_six = step_five

    print('step_six es {}'.format(step_six))
    clabe = initial_clabe+step_six

    print('La clabe es')
    print(clabe)


if __name__ == "__main__":
    # SPEI participant receiver key
    claveSpei = input("what is the SPEI participant key identifier?")

    # 3 digits from Plaza number where the account was opened
    plaza = input("what is the customer plaza?")

    # 11 digits from the account or contract of the customer
    accountNumber = input("what is the customer account/contract number?")

    calculateCheckerDigit(claveSpei, plaza, accountNumber)
