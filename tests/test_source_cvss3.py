import pytest

from sqlalchemy.exc import IntegrityError

from arepo.models.source import SourceModel
from arepo.models.common.scoring.cvss3 import CVSS3Model, CVSS3AssociationModel

# "https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2022-25854"
cvss3_data = [
    {
        "source": "nvd@nist.gov",
        "type": "Primary",
        "cvssData": {
            "version": "3.1",
            "vectorString": "CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:L/I:L/A:N",
            "attackVector": "NETWORK",
            "attackComplexity": "LOW",
            "privilegesRequired": "LOW",
            "userInteraction": "REQUIRED",
            "scope": "CHANGED",
            "confidentialityImpact": "LOW",
            "integrityImpact": "LOW",
            "availabilityImpact": "NONE",
            "baseScore": 5.4,
            "baseSeverity": "MEDIUM"
        },
        "exploitabilityScore": 2.3,
        "impactScore": 2.7
    },
    {
        "source": "report@snyk.io",
        "type": "Secondary",
        "cvssData": {
            "version": "3.1",
            "vectorString": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:L/A:N",
            "attackVector": "NETWORK",
            "attackComplexity": "LOW",
            "privilegesRequired": "NONE",
            "userInteraction": "REQUIRED",
            "scope": "UNCHANGED",
            "confidentialityImpact": "LOW",
            "integrityImpact": "LOW",
            "availabilityImpact": "NONE",
            "baseScore": 5.4,
            "baseSeverity": "MEDIUM"
        },
        "exploitabilityScore": 2.8,
        "impactScore": 2.5
    }
]


@pytest.mark.dependency(depends=["test_insert_source", "test_insert_vulnerability"])
@pytest.mark.dependency(name="test_insert_cvss3")
def test_insert_cvss3(database_session):
    for i, cvss_data in enumerate(cvss3_data):
        source_id = database_session.query(SourceModel).filter_by(email=cvss_data['source']).first().id

        try:
            cvss3_instance = CVSS3Model(
                id=f"test-cvss3-id-{i}",
                version=cvss_data['cvssData']['version'],
                vector_string=cvss_data['cvssData']['vectorString'],
                attack_vector=cvss_data['cvssData']['attackVector'],
                attack_complexity=cvss_data['cvssData']['attackComplexity'],
                privileges_required=cvss_data['cvssData']['privilegesRequired'],
                user_interaction=cvss_data['cvssData']['userInteraction'],
                scope=cvss_data['cvssData']['scope'],
                confidentiality_impact=cvss_data['cvssData']['confidentialityImpact'],
                integrity_impact=cvss_data['cvssData']['integrityImpact'],
                availability_impact=cvss_data['cvssData']['availabilityImpact'],
                base_severity=cvss_data['cvssData']['baseSeverity'],
                base_score=cvss_data['cvssData']['baseScore'],
                exploitability_score=cvss_data['exploitabilityScore'],
                impact_score=cvss_data['impactScore'],
            )
            database_session.add(cvss3_instance)
            database_session.commit()

            cvss3_association_instance = CVSS3AssociationModel(
                cvss_id=cvss3_instance.id,
                source_id=source_id,
                vulnerability_id="CVE-2022-25854"
            )

            database_session.add(cvss3_association_instance)
            database_session.commit()
        except IntegrityError:
            database_session.rollback()
            pytest.fail("IntegrityError occurred while inserting vulnerability")


@pytest.mark.dependency(depends=["test_insert_cvss3"])
def test_get_insert_cvss2(database_session):
    for i, cvss_data_v3 in enumerate(cvss3_data):
        cvss3_instance = database_session.query(CVSS3Model).filter_by(id=f"test-cvss3-id-{i}").first()
        assert cvss3_instance is not None
        source_id = database_session.query(SourceModel).filter_by(email=cvss_data_v3['source']).first().id

        cvss3_association_instance = (database_session.query(CVSS3AssociationModel)
                                      .filter_by(cvss_id=cvss3_instance.id)
                                      .filter_by(source_id=source_id)
                                      .filter_by(vulnerability_id="CVE-2022-25854")
                                      .first())

        assert cvss3_association_instance is not None
