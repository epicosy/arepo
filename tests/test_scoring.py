import pytest

from arepo.models.common.scoring import CVSS3Model, CVSS2Model
from tests.test_vulnerability import vulnerability_data
from sqlalchemy.exc import IntegrityError

# "https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2022-25854"
metric_data = {
          "cvssMetricV31": [
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
          ],
          "cvssMetricV2": [
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
        }


@pytest.mark.dependency(depends=["test_insert_vulnerability"])
@pytest.mark.dependency(name="test_insert_CVSS3")
def test_insert_CVSS3(database_session):
    for i, cvss_data in enumerate(metric_data["cvssMetricV31"]):
        try:
            cvss3_instance = CVSS3Model(
                                    id=f"test-cvss3-id-{i}",
                                    type=cvss_data['type'],
                                    exploitabilityScore=cvss_data['exploitabilityScore'],
                                    impactScore=cvss_data['impactScore'],
                                    cvssData_version=cvss_data['cvssData']['version'],
                                    cvssData_vectorString=cvss_data['cvssData']['vectorString'],
                                    cvssData_attackVector=cvss_data['cvssData']['attackVector'],
                                    cvssData_attackComplexity=cvss_data['cvssData']['attackComplexity'],
                                    cvssData_privilegesRequired=cvss_data['cvssData']['privilegesRequired'],
                                    cvssData_userInteraction=cvss_data['cvssData']['userInteraction'],
                                    cvssData_scope=cvss_data['cvssData']['scope'],
                                    cvssData_confidentialityImpact=cvss_data['cvssData']['confidentialityImpact'],
                                    cvssData_integrityImpact=cvss_data['cvssData']['integrityImpact'],
                                    cvssData_availabilityImpact=cvss_data['cvssData']['availabilityImpact'],
                                    cvssData_baseScore=cvss_data['cvssData']['baseScore'],
                                    cvssData_baseSeverity=cvss_data['cvssData']['baseSeverity'],
                                    vulnerability_id = vulnerability_data["cve"]["id"],
                                )
                    
            database_session.add(cvss3_instance)
            database_session.commit()
        except IntegrityError:
            database_session.rollback()
            pytest.fail("IntegrityError occurred while inserting vulnerability")

        
@pytest.mark.dependency(depends=["test_insert_vulnerability"])
@pytest.mark.dependency(name="test_insert_CVSS2")
def test_insert_CVSS2(database_session):
    for i, cvss_data_v2 in enumerate(metric_data["cvssMetricV2"]):
        try:
          
            cvss2_instance = CVSS2Model(
                                    id=f"test-cvss2-id-{i}",
                                    type=cvss_data_v2['type'],
                                    cvssData_version=cvss_data_v2['cvssData']['version'],
                                    cvssData_vectorString=cvss_data_v2['cvssData']['vectorString'],
                                    cvssData_accessVector=cvss_data_v2['cvssData']['accessVector'],
                                    cvssData_accessComplexity=cvss_data_v2['cvssData']['accessComplexity'],
                                    cvssData_authentication=cvss_data_v2['cvssData']['authentication'],
                                    cvssData_confidentialityImpact=cvss_data_v2['cvssData']['confidentialityImpact'],
                                    cvssData_integrityImpact=cvss_data_v2['cvssData']['integrityImpact'],
                                    cvssData_availabilityImpact=cvss_data_v2['cvssData']['availabilityImpact'],
                                    cvssData_baseScore=cvss_data_v2['cvssData']['baseScore'],
                                    baseSeverity=cvss_data_v2['baseSeverity'],
                                    exploitabilityScore=cvss_data_v2['exploitabilityScore'],
                                    impactScore=cvss_data_v2['impactScore'],
                                    acInsufInfo=cvss_data_v2['acInsufInfo'],
                                    obtainAllPrivilege=cvss_data_v2['obtainAllPrivilege'],
                                    obtainUserPrivilege=cvss_data_v2['obtainUserPrivilege'],
                                    obtainOtherPrivilege=cvss_data_v2['obtainOtherPrivilege'],
                                    userInteractionRequired=cvss_data_v2['userInteractionRequired'],
                                    vulnerability_id = vulnerability_data["cve"]["id"],
                        )
                    
            database_session.add(cvss2_instance)
            database_session.commit()
        except IntegrityError:
            database_session.rollback()
            pytest.fail("IntegrityError occurred while inserting vulnerability")
