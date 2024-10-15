import pytest

from sqlalchemy.exc import IntegrityError

from arepo.models.source import SourceModel
from arepo.models.common.scoring.cvss2 import CVSS2Model, CVSS2AssociationModel


cvss2_data = [
    {
        "source": "nvd@nist.gov",
        "type": "Primary",
        "cvssData": {
            "version": "2.0",
            "vectorString": "AV:N/AC:M/Au:S/C:N/I:P/A:N",
            "accessVector": "NETWORK",
            "accessComplexity": "MEDIUM",
            "authentication": "SINGLE",
            "confidentialityImpact": "NONE",
            "integrityImpact": "PARTIAL",
            "availabilityImpact": "NONE",
            "baseScore": 3.5
        },
        "baseSeverity": "LOW",
        "exploitabilityScore": 6.8,
        "impactScore": 2.9,
        "acInsufInfo": False,
        "obtainAllPrivilege": False,
        "obtainUserPrivilege": False,
        "obtainOtherPrivilege": False,
        "userInteractionRequired": True
    }
]


@pytest.mark.dependency(depends=["test_insert_source", "test_insert_vulnerability"])
@pytest.mark.dependency(name="test_insert_cvss2")
def test_insert_cvss2(database_session):
    for i, cvss_data_v2 in enumerate(cvss2_data):
        source_id = database_session.query(SourceModel).filter_by(email=cvss_data_v2['source']).first().id

        try:
            cvss2_instance = CVSS2Model(
                id=f"test-cvss2-id-{i}",
                vector_string=cvss_data_v2['cvssData']['vectorString'],
                access_vector=cvss_data_v2['cvssData']['accessVector'],
                access_complexity=cvss_data_v2['cvssData']['accessComplexity'],
                authentication=cvss_data_v2['cvssData']['authentication'],
                confidentiality_impact=cvss_data_v2['cvssData']['confidentialityImpact'],
                integrity_impact=cvss_data_v2['cvssData']['integrityImpact'],
                availability_impact=cvss_data_v2['cvssData']['availabilityImpact'],
                base_severity=cvss_data_v2['baseSeverity'],
                base_score=cvss_data_v2['cvssData']['baseScore'],
                exploitability_score=cvss_data_v2['exploitabilityScore'],
                impact_score=cvss_data_v2['impactScore'],
                ac_insuf_info=cvss_data_v2['acInsufInfo'],
                obtain_all_privilege=cvss_data_v2['obtainAllPrivilege'],
                obtain_user_privilege=cvss_data_v2['obtainUserPrivilege'],
                obtain_other_privilege=cvss_data_v2['obtainOtherPrivilege'],
                user_interaction_required=cvss_data_v2['userInteractionRequired']
            )
            database_session.add(cvss2_instance)
            database_session.commit()

            cvss2_association_instance = CVSS2AssociationModel(
                cvss_id=cvss2_instance.id,
                source_id=source_id,
                vulnerability_id="CVE-2022-25854"
            )

            database_session.add(cvss2_association_instance)
            database_session.commit()
        except IntegrityError:
            database_session.rollback()
            pytest.fail("IntegrityError occurred while inserting vulnerability")


@pytest.mark.dependency(depends=["test_insert_cvss2"])
def test_get_insert_cvss2(database_session):
    for i, cvss_data_v2 in enumerate(cvss2_data):
        cvss2_instance = database_session.query(CVSS2Model).filter_by(id=f"test-cvss2-id-{i}").first()
        assert cvss2_instance is not None
        source_id = database_session.query(SourceModel).filter_by(email=cvss_data_v2['source']).first().id

        cvss2_association_instance = (database_session.query(CVSS2AssociationModel)
                                      .filter_by(cvss_id=cvss2_instance.id)
                                      .filter_by(source_id=source_id)
                                      .filter_by(vulnerability_id="CVE-2022-25854")
                                      .first())

        assert cvss2_association_instance is not None
