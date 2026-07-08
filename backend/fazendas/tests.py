from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import Usuario
from .models import Fazenda, AcessoFazenda


class FazendaApiTests(APITestCase):
    def setUp(self):
        self.produtor = Usuario.objects.create_user(
            email='produtor@agrocore.com',
            nome='Produtor Teste',
            password='12345678',
            aprovado=True,
            perfil=Usuario.Perfil.PRODUTOR,
        )
        self.funcionario = Usuario.objects.create_user(
            email='funcionario@agrocore.com',
            nome='Funcionário Teste',
            password='12345678',
            aprovado=True,
            perfil=Usuario.Perfil.OPERADOR,
        )
        self.client.force_authenticate(user=self.produtor)

    def test_produtor_lista_somente_suas_fazendas(self):
        Fazenda.objects.create(nome='Fazenda A', produtor=self.produtor)
        outra = Usuario.objects.create_user(
            email='outro@agrocore.com',
            nome='Outro',
            password='12345678',
            aprovado=True,
            perfil=Usuario.Perfil.PRODUTOR,
        )
        Fazenda.objects.create(nome='Fazenda B', produtor=outra)

        response = self.client.get(reverse('fazenda-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nome'], 'Fazenda A')

    def test_cria_acesso_para_funcionario_na_fazenda(self):
        fazenda = Fazenda.objects.create(nome='Fazenda A', produtor=self.produtor)

        response = self.client.post(
            reverse('acesso-list'),
            {
                'fazenda': fazenda.id,
                'email': self.funcionario.email,
                'perfil': 'operador',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            AcessoFazenda.objects.filter(fazenda=fazenda, usuario=self.funcionario).exists()
        )
