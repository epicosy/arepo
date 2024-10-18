import pandas as pd
import hashlib
from pathlib import Path

from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine

from arepo.models.bf import BFClassModel, OperationModel, PhaseModel
from arepo.models.common.tag import TagModel
from arepo.models.common.platform.vendor import VendorModel
from arepo.models.common.weakness import (AbstractionModel, GroupingModel, CWEModel, CWEOperationModel, CWEPhaseModel,
                                          CWEBFClassModel)


tables_path = Path(__file__).parent / 'tables'
TABLE_NAMES = {
    TagModel.__tablename__: TagModel, AbstractionModel.__tablename__: AbstractionModel,
    BFClassModel.__tablename__: BFClassModel, OperationModel.__tablename__: OperationModel,
    PhaseModel.__tablename__: PhaseModel, CWEModel.__tablename__: CWEModel, VendorModel.__tablename__: VendorModel
}


class ArepoError(Exception):
    """Generic errors."""
    pass


def populate(engine: Engine):
    """Clear the existing data and create new tables."""
    print('Initializing the database.')

    with Session(engine) as session, session.begin():

        if not session.query(AbstractionModel).all():
            abstractions_df = pd.read_csv(f'{tables_path}/abstractions.csv')
            session.add_all([AbstractionModel(**row.to_dict()) for i, row in abstractions_df.iterrows()])
            print("Populated 'abstractions' table.")

        if not session.query(TagModel).all():
            tags_df = pd.read_csv(f'{tables_path}/tags.csv')
            session.add_all([TagModel(**row.to_dict()) for i, row in tags_df.iterrows()])
            print("Populated 'tags' table.")

        if not session.query(OperationModel).all():
            operations_df = pd.read_csv(f'{tables_path}/operations.csv')
            session.add_all([OperationModel(**row.to_dict()) for i, row in operations_df.iterrows()])
            print("Populated 'operations' table.")

        if not session.query(PhaseModel).all():
            phases_df = pd.read_csv(f'{tables_path}/phases.csv')
            session.add_all([PhaseModel(**row.to_dict()) for i, row in phases_df.iterrows()])
            print("Populated 'phases' table.")

        if not session.query(BFClassModel).all():
            classes_df = pd.read_csv(f'{tables_path}/bf_classes.csv')
            session.add_all([BFClassModel(**row.to_dict()) for i, row in classes_df.iterrows()])
            print("Populated 'bf_classes' table.")

        if not session.query(CWEModel).all():
            cwes_df = pd.read_csv(f'{tables_path}/cwes.csv')
            session.add_all([CWEModel(**row.to_dict()) for i, row in cwes_df.iterrows()])
            print("Populated 'cwes' table.")

        if not session.query(CWEOperationModel).all():
            cwe_operations_df = pd.read_csv(f'{tables_path}/cwe_operation.csv')
            session.add_all([CWEOperationModel(**row.to_dict()) for i, row in cwe_operations_df.iterrows()])
            print("Populated 'cwe_operations' table.")

        if not session.query(CWEPhaseModel).all():
            cwe_phases_df = pd.read_csv(f'{tables_path}/cwe_phase.csv')
            session.add_all([CWEPhaseModel(**row.to_dict()) for i, row in cwe_phases_df.iterrows()])
            print("Populated 'cwe_phases' table.")

        if not session.query(CWEBFClassModel).all():
            cwe_bf_classes_df = pd.read_csv(f'{tables_path}/cwe_class.csv')
            session.add_all([CWEBFClassModel(**row.to_dict()) for i, row in cwe_bf_classes_df.iterrows()])
            print("Populated 'cwe_bf_classes' table.")

        if not session.query(VendorModel).all():
            vendors_df = pd.read_csv(f'{tables_path}/vendor_product_type.csv')['vendor'].unique()
            session.add_all([VendorModel(id=hashlib.md5(vendor.encode('utf-8')).hexdigest(),
                                         name=vendor) for vendor in vendors_df])
            print("Populated 'vendors' table.")

        if not session.query(GroupingModel).all():
            grouping_df = pd.read_csv(f'{tables_path}/groupings.csv')
            session.add_all([GroupingModel(**row.to_dict()) for i, row in grouping_df.iterrows()])
            print("Populated 'grouping' table.")

        session.commit()


def get_digest(string: str):
    return hashlib.md5(string.encode('utf-8')).hexdigest()
