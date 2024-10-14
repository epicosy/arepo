import pytest
import hashlib

from arepo.models.common.vulnerability import ReferenceModel, ReferenceTagModel, TagModel, ReferenceVulnerabilityModel

reference_data = [
    {
      "url": "https://bsg.tech/blog/cve-2022-25854-stored-xss-in-yaireo-tagify-npm-module/",
      "source": "report@snyk.io",
      "tags": [
        "Exploit",
        "Patch",
        "Third Party Advisory"
      ]
    },
    {
      "url": "https://github.com/yairEO/tagify/commit/198c0451fad188390390395ccfc84ab371def4c7",
      "source": "report@snyk.io",
      "tags": [
        "Patch",
        "Third Party Advisory"
      ]
    },
    {
      "url": "https://github.com/yairEO/tagify/issues/988",
      "source": "report@snyk.io",
      "tags": [
        "Exploit",
        "Issue Tracking",
        "Third Party Advisory"
      ]
    },
    {
      "url": "https://github.com/yairEO/tagify/releases/tag/v4.9.8",
      "source": "report@snyk.io",
      "tags": [
        "Release Notes",
        "Third Party Advisory"
      ]
    },
    {
      "url": "https://snyk.io/vuln/SNYK-JS-YAIREOTAGIFY-2404358",
      "source": "report@snyk.io",
      "tags": [
        "Third Party Advisory"
      ]
    }
]


# change the format of the reference data to be a dict with ids
reference_data = {hashlib.md5(reference["url"].encode('utf-8')).hexdigest(): reference for reference in reference_data}


@pytest.mark.dependency(depends=["test_insert_vulnerability"])
@pytest.mark.dependency(name="test_insert_references")
def test_insert_references(database_session):
    from sqlalchemy.exc import IntegrityError
    tag_ids = {tag.name: tag.id for tag in database_session.query(TagModel).all()}

    for _id, reference in reference_data.items():
        try:
            # Creating ReferenceModel object
            reference_model = ReferenceModel(
                id=_id,
                url=reference["url"],
                source=reference["source"]
            )

            database_session.add(reference_model)
            database_session.commit()

            for tag in reference["tags"]:
                # Creating ReferenceTagModel object
                reference_tag = ReferenceTagModel(
                    reference_id=_id,
                    tag_id=tag_ids[tag]
                )

                database_session.add(reference_tag)
                database_session.commit()

            # Creating ReferenceVulnerabilityModel object
            reference_vulnerability = ReferenceVulnerabilityModel(
                reference_id=_id,
                vulnerability_id="CVE-2022-25854"
            )

            database_session.add(reference_vulnerability)
            database_session.commit()
        except IntegrityError:
            database_session.rollback()
            pytest.fail("IntegrityError occurred while inserting references")


@pytest.mark.dependency(depends=["test_insert_references"])
def test_get_inserted_references(database_session):
    # Query the database to retrieve the inserted references
    retrieved_references = database_session.query(ReferenceModel).all()
    tag_ids = [tag.id for tag in database_session.query(TagModel).all()]

    # Check if the retrieved references exist
    assert retrieved_references is not None
    assert len(retrieved_references) == len(reference_data)

    for reference in retrieved_references:
        # Assert the retrieved data matches the expected values
        assert reference.url == reference_data[reference.id]["url"]
        assert reference.source == reference_data[reference.id]["source"]

        # Query the database to retrieve the inserted reference tags
        retrieved_reference_tags = database_session.query(ReferenceTagModel).filter_by(reference_id=reference.id).all()

        # Check if the retrieved reference tags exist
        assert retrieved_reference_tags is not None
        assert len(retrieved_reference_tags) == len(reference_data[reference.id]["tags"])

        for reference_tag in retrieved_reference_tags:
            # Assert the retrieved data matches the expected values
            assert reference_tag.tag_id in tag_ids

    # Query the database to retrieve the inserted reference vulnerabilities
    retrieved_reference_vulnerabilities = database_session.query(ReferenceVulnerabilityModel).all()

    # Check if the retrieved reference vulnerabilities exist
    assert retrieved_reference_vulnerabilities is not None
    assert len(retrieved_reference_vulnerabilities) == len(reference_data)

    for reference_vulnerability in retrieved_reference_vulnerabilities:
        # Assert the retrieved data matches the expected values
        assert reference_vulnerability.vulnerability_id == "CVE-2022-25854"
        assert reference_vulnerability.reference_id in [ref.id for ref in retrieved_references]
