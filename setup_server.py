import click

from app.models import create_tables, create_user, update_user, populate_tables, \
    User, db


@click.group()
def dbcli():
    pass


@dbcli.command()
@click.option('--create', is_flag=True)
@click.option('--populate', is_flag=True)
def database(create, populate):
    if create:
        click.confirm(
            'Do you want to create new tables, this will destroy all data',
            abort=True)
        if create_tables():
            click.echo("Tables have been created")
        else:
            click.echo("Tables could not be created")
    if populate:
        populate_tables()


@click.group()
def usercli():
    pass


@usercli.command()
def change_email():
    old_email = click.prompt('Enter your old email address')
    if not User.get(User.email == old_email):
        click.echo(
            'The email address {email} does not exist'.format(email=old_email)
        )

    new_email = click.prompt('Enter your new email address')
    click.confirm(
        'You old email was {old_email}, your new email will be {new_email}'
        .format(old_email=old_email,
                new_email=new_email),
        abort=True)
    update_user(old_email=old_email, new_email=new_email)


@usercli.command()
@click.option('--email', prompt='Your email address')
@click.password_option()
def change_password(email, password):
    update_user(email, password=password)


@usercli.command()
@click.option('--email', prompt='Enter your new email address')
@click.password_option()
def new_user(email, password):
    create_user(email, password)


@usercli.command()
def delete_user():
    email = click.prompt('Which user do you want to delete')
    if click.confirm(
            'Are you sure you want to delete {email}?'.format(email=email)):
        try:
            User.get(User.email == email).delete_instance()
        except User.DoesNotExist:
            click.echo(
                'The user with email address {email} does not exist'.format(
                    email=email))


cli = click.CommandCollection(sources=[dbcli, usercli])

if __name__ == "__main__":
    db.init('app/blog.db')
    cli()
