import pytest

from sqlalchemy.exc import IntegrityError

from arepo.models.common.platform.product import ProductModel
from arepo.models.common.platform.vendor import VendorModel
from arepo.models.common.platform.cpe import CPEMatchModel, CPEModel
from arepo.models.common.platform.configuration import ConfigurationModel, NodeModel


config_data = [
    {
        "id": "config_id",
        "is_vulnerable": True,
        "is_multi_component": False,
        "is_platform_specific": False
    }
]

node_data = [
    {
        "id": "node_id",
        "configuration_id": "config_id",
        "operator": "OR",
        "negate": False,
        "is_vulnerable": True,
        "is_multi_component": False,
        "is_context_dependent": False
    }
]

cpe_match_data = [
    {
        "cpe_id": "cpe_id",
        "node_id": "node_id",
        "vulnerable": True,
        "versionEndExcluding": "4.9.8",
        "matchCriteriaId": "135622D7-7891-420D-81D9-C078AD572C78"
    }
]

cpe_data = [
    {
        "id": "cpe_id",
        "criteria": ":a:tagify_project:tagify:*:*:*:*:*:*:*:*"
    }
]


@pytest.mark.dependency(name="test_platform_configuration")
def test_platform_configuration(database_session):
    for config in config_data:
        try:
            configuration = ConfigurationModel(
                id=config['id'],
                vulnerability_id="CVE-2022-25854",
                is_vulnerable=config['is_vulnerable'],
                is_multi_component=config['is_multi_component'],
                is_platform_specific=config['is_platform_specific']
            )

            database_session.add(configuration)
            database_session.commit()
        except IntegrityError:
            database_session.rollback()
            pytest.fail("IntegrityError occurred while inserting configuration")


@pytest.mark.dependency(name="test_platform_vendor")
def test_platform_vendor(database_session):
    try:
        vendor = VendorModel(
            id="vendor_id",
            name="tagify_project"
        )

        database_session.add(vendor)
        database_session.commit()
    except IntegrityError:
        database_session.rollback()
        pytest.fail("IntegrityError occurred while inserting vendor")


@pytest.mark.dependency(depends=["test_platform_vendor"])
@pytest.mark.dependency(name="test_platform_product")
def test_platform_product(database_session):
    try:
        vendor_id = database_session.query(VendorModel).filter_by(name="tagify_project").first().id

        product = ProductModel(
            id="product_id",
            part="a",
            name="tagify",
            vendor_id=vendor_id
        )

        database_session.add(product)
        database_session.commit()
    except IntegrityError:
        database_session.rollback()
        pytest.fail("IntegrityError occurred while inserting product")


@pytest.mark.dependency(depends=["test_platform_product"])
@pytest.mark.dependency(name="test_cpe")
def test_cpe(database_session):
    try:
        product_id = database_session.query(ProductModel).filter_by(name="tagify").first().id

        cpe = CPEModel(
            id="cpe_id",
            product_id=product_id
        )

        database_session.add(cpe)
        database_session.commit()
    except IntegrityError:
        database_session.rollback()
        pytest.fail("IntegrityError occurred while inserting CPE")


@pytest.mark.dependency(depends=["test_platform_configuration"])
@pytest.mark.dependency(name="test_configuration_node")
def test_configuration_node(database_session):
    for node in node_data:
        config_id = database_session.query(ConfigurationModel).filter_by(id="config_id").first().id

        try:
            node = NodeModel(
                id="node_id",
                configuration_id=config_id,
                operator=node['operator'],
                negate=node['negate'],
                is_vulnerable=node['is_vulnerable'],
                is_multi_component=node['is_multi_component'],
                is_context_dependent=node['is_context_dependent']
            )

            database_session.add(node)
            database_session.commit()
        except IntegrityError:
            database_session.rollback()
            pytest.fail("IntegrityError occurred while inserting node")


@pytest.mark.dependency(depends=["test_cpe", "test_configuration_node"])
@pytest.mark.dependency(name="test_cpe_match")
def test_cpe_match(database_session):
    for cpe_match in cpe_match_data:
        cpe_id = database_session.query(CPEModel).filter_by(id="cpe_id").first().id
        node_id = database_session.query(NodeModel).filter_by(id="node_id").first().id

        try:
            cpe_match = CPEMatchModel(
                id=cpe_match['matchCriteriaId'],
                cpe_id=cpe_id,
                node_id=node_id,
                vulnerable=cpe_match['vulnerable'],
                version_end_excluding=cpe_match['versionEndExcluding']
            )

            database_session.add(cpe_match)
            database_session.commit()
        except IntegrityError:
            database_session.rollback()
            pytest.fail("IntegrityError occurred while inserting CPE Match")
