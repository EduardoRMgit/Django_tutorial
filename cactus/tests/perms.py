def load_groups(verbose=False):
    if verbose:
        print("Loading groups and perms")

    from django.contrib.auth.models import Permission, Group

    new_group = Group.objects.get_or_create(name='Administradores')[0]

    perms = ["view_user", "add_user", "change_user", "delete_user",
             "view_group", "add_group", "change_group", "delete_group",
             "view_Token", "add_Token", "change_Token",
             "delete_Token",
             "view_refreshtoken", "add_refreshtoken", "change_refreshtoken",
             "delete_refreshtoken",
             "view_permission", "add_permission", "change_permission",
             "delete_permission",
             "view_profilecomponent", "add_profilecomponent",
             "change_profilecomponent",
             "delete_profilecomponent"]
    q = Permission.objects.all()

    for x in perms:
        q = q.exclude(codename__contains=x)

    new_group.permissions.clear()
    for perm in q:
        new_group.permissions.add(perm)

    new_group.save()
    if verbose:
        print("Done admin")

    new_group2 = Group.objects.get_or_create(name='PLD')[0]

    perms2 = ["demograficos", "PLD"]
    q = Permission.objects.filter(content_type__app_label__contains=perms2[0])

    for x in perms2:
        j = Permission.objects.filter(content_type__app_label__contains=x)
        q = (q | j)

    new_group2.permissions.clear()

    for perm in q:
        new_group2.permissions.add(perm)

    new_group2.save()

    if verbose:
        print("Done PLD")

    new_group3 = Group.objects.get_or_create(name='Finanzas')[0]

    perms3 = ["banca", "spei", "contabilidad"]
    q = Permission.objects.filter(content_type__app_label__contains=perms3[0])

    for x in perms3:
        j = Permission.objects.filter(content_type__app_label__contains=x)
        q = (q | j)

    new_group3.permissions.clear()

    for perm in q:
        new_group3.permissions.add(perm)

    new_group3.save()
    if verbose:
        print("Done Finanzas")

    new_group4 = Group.objects.get_or_create(name='Operativo')[0]

    perms4 = ["administradore", "banca", "demograficos", "servicios", "dde",
              "django_db_logger"]
    q = Permission.objects.filter(content_type__app_label__contains=perms4[0])

    for x in perms4:
        j = Permission.objects.filter(content_type__app_label__contains=x)
        q = (q | j)

    new_group4.permissions.clear()

    for perm in q:
        new_group4.permissions.add(perm)

    new_group4.save()
    if verbose:
        print("Done Operativo")

    new_group5 = Group.objects.get_or_create(name='ServicioClient')[0]

    perms5 = ["demograficos", "banca"]
    q = Permission.objects.filter(content_type__app_label__contains=perms5[0])

    for x in perms5:
        j = Permission.objects.filter(content_type__app_label__contains=x)
        q = (q | j)

    new_group5.permissions.clear()

    for perm in q:
        new_group5.permissions.add(perm)

    new_group5.save()
    if verbose:
        print("Done ServicioClient")


if __name__ == "__main__" or __name__ == \
     'django.core.management.commands.shell':
    load_groups(verbose=True)
