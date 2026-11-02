"""One strict generator batch interface, shared by schema emission and DAG checks."""
from __future__ import annotations
from typing import Literal
from pydantic import BaseModel,ConfigDict,Field,TypeAdapter,model_validator
import lineage


class Parent(BaseModel):
    model_config=ConfigDict(extra='forbid',strict=True)
    attempt_id:str=Field(min_length=1)
    contribution:str=Field(min_length=1)


class ScientificConfig(BaseModel):
    model_config=ConfigDict(extra='forbid',strict=True)
    scope:Literal['primary216','confirmatory207','panel242_reference_filtered','tmod1_alias208']
    operator:Literal['mean_abs_delta','abs_mean_delta','max_abs_delta']
    adjust:Literal['none','base_strength','base_plus_organoid_mean']


class Candidate(BaseModel):
    model_config=ConfigDict(extra='forbid',strict=True)
    origin:Literal['new','refinement','underexplored_extension','combination','repair']
    parents:list[Parent]
    config:ScientificConfig
    direction_id:str=Field(min_length=1)
    priority:float=Field(ge=0,le=1)
    bottleneck:str=Field(min_length=1)
    evidence_attempt_ids:list[str]
    repairs_node:str|None=None
    fix_class:Literal['bug_fix','support_fix','legalization','numeric_fix']|None=None

    @model_validator(mode='after')
    def parent_semantics(self):
        ids=[p.attempt_id for p in self.parents]
        if any(not p.attempt_id.strip() or not p.contribution.strip() for p in self.parents):
            raise ValueError('nonempty parent IDs and contributions required')
        if len(ids)!=len(set(ids)):
            raise ValueError('duplicate parent IDs')
        lo,hi=lineage.ORIGINS[self.origin]
        if not lo<=len(ids)<=hi:
            raise ValueError(f'origin {self.origin} requires {lo}..{hi} parents')
        if self.origin=='repair' and (self.repairs_node not in ids or self.fix_class is None):
            raise ValueError('repair requires a cited parent and named fix_class')
        return self


Batch=TypeAdapter(list[Candidate])


def schema():
    result=Batch.json_schema()
    result.update(minItems=1,maxItems=40)
    return result


def validate_batch(payload,existing:dict,study_id:str,evaluator_version:str):
    candidates=Batch.validate_python(payload)
    if not 1<=len(candidates)<=40:raise ValueError('batch size outside1..40')
    validated=[]
    for i,c in enumerate(candidates):
        node={**c.model_dump(exclude_none=True),'attempt_id':f'proposal-{i}',
              'study_id':study_id,'evaluator_version':evaluator_version}
        errors=lineage.validate_node(node,existing)
        unknown=set(c.evidence_attempt_ids)-set(existing)
        if unknown:errors.append(f'evidence IDs absent from admissible history:{sorted(unknown)}')
        for record_id in set(c.evidence_attempt_ids)&set(existing):
            if existing[record_id].get('study_id')!=study_id or existing[record_id].get('evaluator_version')!=evaluator_version:
                errors.append(f'evidence ID study/evaluator mismatch:{record_id}')
        if errors:raise ValueError(';'.join(errors))
        validated.append(c.model_dump(exclude_none=True))
    return validated
