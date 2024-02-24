import pandas as pd
import hashlib
from pathlib import Path

from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine

from arepo.models.common.vulnerability import Tag
from arepo.models.bf import BFClass, Operation, Phase
from arepo.models.common.platform import ProductType, Vendor, Product
from arepo.models.common.weakness import Abstraction, Grouping, CWE, CWEOperation, CWEPhase, CWEBFClass


tables_path = Path(__file__).parent / 'tables'


class ArepoError(Exception):
    """Generic errors."""
    pass


def populate(engine: Engine):
    """Clear the existing data and create new tables."""
    print('Initializing the database.')

    with Session(engine) as session, session.begin():

        if not session.query(Abstraction).all():
            abstractions_df = pd.read_csv(f'{tables_path}/abstractions.csv')
            session.add_all([Abstraction(**row.to_dict()) for i, row in abstractions_df.iterrows()])
            print("Populated 'abstractions' table.")

        if not session.query(Tag).all():
            tags_df = pd.read_csv(f'{tables_path}/tags.csv')
            session.add_all([Tag(**row.to_dict()) for i, row in tags_df.iterrows()])
            print("Populated 'tags' table.")

        if not session.query(Operation).all():
            operations_df = pd.read_csv(f'{tables_path}/operations.csv')
            session.add_all([Operation(**row.to_dict()) for i, row in operations_df.iterrows()])
            print("Populated 'operations' table.")

        if not session.query(Phase).all():
            phases_df = pd.read_csv(f'{tables_path}/phases.csv')
            session.add_all([Phase(**row.to_dict()) for i, row in phases_df.iterrows()])
            print("Populated 'phases' table.")

        if not session.query(BFClass).all():
            classes_df = pd.read_csv(f'{tables_path}/bf_classes.csv')
            session.add_all([BFClass(**row.to_dict()) for i, row in classes_df.iterrows()])
            print("Populated 'bf_classes' table.")

        if not session.query(CWE).all():
            cwes_df = pd.read_csv(f'{tables_path}/cwes.csv')
            session.add_all([CWE(**row.to_dict()) for i, row in cwes_df.iterrows()])
            print("Populated 'cwes' table.")

        if not session.query(CWEOperation).all():
            cwe_operations_df = pd.read_csv(f'{tables_path}/cwe_operation.csv')
            session.add_all([CWEOperation(**row.to_dict()) for i, row in cwe_operations_df.iterrows()])
            print("Populated 'cwe_operations' table.")

        if not session.query(CWEPhase).all():
            cwe_phases_df = pd.read_csv(f'{tables_path}/cwe_phase.csv')
            session.add_all([CWEPhase(**row.to_dict()) for i, row in cwe_phases_df.iterrows()])
            print("Populated 'cwe_phases' table.")

        if not session.query(CWEBFClass).all():
            cwe_bf_classes_df = pd.read_csv(f'{tables_path}/cwe_class.csv')
            session.add_all([CWEBFClass(**row.to_dict()) for i, row in cwe_bf_classes_df.iterrows()])
            print("Populated 'cwe_bf_classes' table.")

        if not session.query(ProductType).all():
            product_types_df = pd.read_csv(f'{tables_path}/product_type.csv')
            session.add_all([ProductType(**row.to_dict()) for i, row in product_types_df.iterrows()])
            print("Populated 'product_types' table.")

        if not session.query(Vendor).all():
            vendors_df = pd.read_csv(f'{tables_path}/vendor_product_type.csv')['vendor'].unique()
            session.add_all([Vendor(id=hashlib.md5(vendor.encode('utf-8')).hexdigest(),
                                    name=vendor) for vendor in vendors_df])
            print("Populated 'vendors' table.")

        if not session.query(Product).all():
            vendor_product_type = pd.read_csv(f'{tables_path}/vendor_product_type.csv')
            data = []

            for g, _ in vendor_product_type.groupby(['vendor', 'product', 'product_type']):
                vendor, product, product_type = g
                product = str(product)
                product_type = int(product_type)
                vendor_id = hashlib.md5(vendor.encode('utf-8')).hexdigest()
                product_id = hashlib.md5(f"{vendor}:{product}".encode('utf-8')).hexdigest()

                # convert product to utf-8
                data.append(Product(id=product_id, name=product, vendor_id=vendor_id, product_type_id=product_type))

            session.add_all(data)
            print("Populated 'products' table.")

        if not session.query(Grouping).all():
            grouping_df = pd.read_csv(f'{tables_path}/groupings.csv')
            session.add_all([Grouping(**row.to_dict()) for i, row in grouping_df.iterrows()])
            print("Populated 'grouping' table.")

        session.commit()
