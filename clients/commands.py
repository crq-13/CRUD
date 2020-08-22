import click

from clients.services import ClientService
from clients.models import ClientModel

@click.group()
def clientes():
    """Manejar el ciclo de los clientes"""
    pass


@clientes.command()
@click.option('-n', '--name',
              type=str,
              prompt=True,
              help='Nombre del cliente')
@click.option('-c', '--company',
              type=str,
              prompt=True,
              help='Empresa del cliente')
@click.option('-e', '--email',
              type=str,
              prompt=True,
              help='Email del cliente')
@click.option('-p', '--position',
              type=str,
              prompt=True,
              help='Nombre del cliente')
@click.pass_context
def create(ctx, name, company, email, position):
    """Crear un nuevo cliente"""
    client = ClientModel(name, company, email, position)
    client_service = ClientService(ctx.obj['clients_table'])

    client_service.create_client(client)


@clientes.command()
@click.pass_context
def list(ctx):
    """Listar todos los clientes"""
    client_service = ClientService(ctx.obj['clients_table'])
    client_list = client_service.list_clients()
    click.echo('  ID     |   NAME    |   COMPANY |   EMAIL   |   POSITION')
    click.echo('*' * 100)

    for client in client_list:
        click.echo('  {uid}     |   {name}    |   {company} |   {email}   |   {position}'.format(
            uid=client['uid'],
            name=client['name'],
            company=client['company'],
            email=client['email'],
            position=client['position']
        ))


@clientes.command()
@click.argument('client_uid',
                type=str)
@click.pass_context
def update(ctx, client_uid):
    """Actualizar un cliente"""
    client_service = ClientService(ctx.obj['clients_table'])
    client_list = client_service.list_clients()
    client = [client for client in client_list if client['uid'] == client_uid]
    if client:
        client = _update_client_flow(ClientModel(**client[0]))
        client_service.update_client(client)

        click.echo('Cliente actualizado')
    else:
        click.echo('No se encontro el cliente')


def _update_client_flow(client):
    click.echo('Dejalo vacio si no quieres modificar el valor')

    client.name = click.prompt('Nuevo nombre', type=str, default=client.name)
    client.company = click.prompt('Nueva empresa', type=str, default=client.company)
    client.email = click.prompt('Nuevo email', type=str, default=client.email)
    client.position = click.prompt('Nueva posicion', type=str, default=client.position)

    return client


@clientes.command()
@click.argument('client_uid',
                type=str)
@click.pass_context
def delete(ctx, client_uid):
    """Eliminar un cliente"""
    client_service = ClientService(ctx.obj['clients_table'])
    clients = client_service.list_clients()
    client = [client for client in clients if client['uid'] == client_uid]
    if client:
        print(client[0])
        client_service.delete_client(client[0])
        click.echo('Cliente borrado')
    else:
        click.echo('No se encontro el cliente')

all = clientes