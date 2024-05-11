# """
# optional 처리로는 fastapi의 requried 필드옵션에 대한 제어가 불가능하다.
# 따라서 직접적인 class 선언및 Field(..., example='xxx') , Field(None) 기능으로 제어하도록 한다.
# """
#
# from typing import Optional, Type
#
# from pydantic import BaseModel, create_model, Field
#
#
# def make_optional(baseclass: Type[BaseModel], exclude=None) -> Type[BaseModel]:
#     if exclude is None:
#         optional_fields = {
#             key: (Optional[item.annotation], None)
#             for key, item in baseclass.model_fields.items()
#         }
#     else:
#         optional_fields = {
#             key: (Optional[item.annotation]
#                   if key not in exclude else
#                   item.annotation,
#                   None)
#             for key, item in baseclass.model_fields.items()
#         }
#     validators = {'__validators__': baseclass.__validators__} \
#         if hasattr(baseclass, '__validators__') else None
#     return create_model(f'{baseclass.__name__}_Optional',
#                         **optional_fields,
#                         __validators__=validators)
#
#
# def make_omit(baseclass: Type[BaseModel], omit_fields) -> Type[BaseModel]:
#     fields = {}
#     for key, item in baseclass.model_fields.items():
#         if key not in omit_fields:
#             fields[key] = (item.annotation, None)
#     validators = {'__validators__': baseclass.__validators__} \
#         if hasattr(baseclass, '__validators__') else None
#     return create_model(f'{baseclass.__name__}_Omit' + ''.join(omit_fields),
#                         **fields,
#                         __validators__=validators)
#
#
# from pydantic._internal._model_construction import ModelMetaclass
#
#
# class MakeOptional(ModelMetaclass):
#     def __new__(self, name, bases, namespaces, **kwargs):
#         optional_exclude_fields = getattr(namespaces.get("Config", {}),
#                                           "optional_exclude_fields",
#                                           {})
#         annotations = namespaces.get('__annotations__', {})
#         for base in bases:
#             annotations.update(base.__annotations__)
#         for field in annotations:
#             if not field.startswith('__') and field not in optional_exclude_fields:
#                 annotations[field] = Optional[annotations[field]]
#         namespaces['__annotations__'] = annotations
#         return super().__new__(self, name, bases, namespaces, **kwargs)
#
#
# class Omit(ModelMetaclass):
#     def __new__(self, name, bases, namespaces, **kwargs):
#         omit_fields = getattr(namespaces.get("Config", {}), "omit_fields", {})
#         fields = namespaces.get('__fields__', {})
#         annotations = namespaces.get('__annotations__', {})
#         for base in bases:
#             fields.update(base.model_fields)
#             annotations.update(base.__annotations__)
#         merged_keys = fields.keys() & annotations.keys()
#         [merged_keys.add(field) for field in fields]
#         new_fields = {}
#         new_annotations = {}
#         for field in merged_keys:
#             if not field.startswith('__') and field not in omit_fields:
#                 new_annotations[field] = annotations.get(field, fields[field].annotation)
#                 new_fields[field] = fields[field]
#         namespaces['__annotations__'] = new_annotations
#         namespaces['__fields__'] = new_fields
#         return super().__new__(self, name, bases, namespaces, **kwargs)
#
#
# class BaseItem(BaseModel):
#     name: str
#     model: str
#     manufacturer: str
#     price: float
#     tax: float
#
#
# class BaseItemOptional(BaseItem, metaclass=MakeOptional):
#     ...
#
#     class Config:
#         optional_exclude_fields = ['name']
#
#
# import pprint
#
# pprint.pprint(BaseItemOptional.__name__)
# pprint.pprint(BaseItemOptional.__fields__)
#
#
# class BaseItem(BaseModel):
#     name: str
#     model: str
#     manufacturer: str
#     price: float
#     tax: float
#
#
# import pprint
#
# pprint.pprint(BaseItem.__fields__)
#
# BaseItemOptional = make_optional(BaseItem, exclude=['model', 'tax'])
#
# pprint.pprint(BaseItemOptional.__name__)
# pprint.pprint(BaseItemOptional.__fields__)
#
# BaseItemOptionalOmitName = make_omit(BaseItemOptional, ['name'])
#
# pprint.pprint(BaseItemOptionalOmitName.__name__)
# pprint.pprint(BaseItemOptionalOmitName.__fields__)
#
# from pydantic._internal._model_construction import ModelMetaclass
#
#
# class AllOptional(ModelMetaclass):
#     def __new__(self, name, bases, namespaces, **kwargs):
#         annotations = namespaces.get('__annotations__', {})
#         for base in bases:
#             annotations.update(base.__annotations__)
#         for field in annotations:
#             if not field.startswith('__'):
#                 annotations[field] = Optional[annotations[field]]
#         namespaces['__annotations__'] = annotations
#         return super().__new__(self, name, bases, namespaces, **kwargs)
#
#
# class Omit(ModelMetaclass):
#     def __new__(self, name, bases, namespaces, **kwargs):
#         omit_fields = getattr(namespaces.get("Config", {}), "omit_fields", {})
#         fields = namespaces.get('__fields__', {})
#         annotations = namespaces.get('__annotations__', {})
#         for base in bases:
#             fields.update(base.model_fields)
#             annotations.update(base.__annotations__)
#         merged_keys = fields.keys() & annotations.keys()
#         [merged_keys.add(field) for field in fields]
#         new_fields = {}
#         new_annotations = {}
#         for field in merged_keys:
#             if not field.startswith('__') and field not in omit_fields:
#                 new_annotations[field] = annotations.get(field, fields[field].annotation)
#                 new_fields[field] = fields[field]
#         namespaces['__annotations__'] = new_annotations
#         namespaces['__fields__'] = new_fields
#         return super().__new__(self, name, bases, namespaces, **kwargs)
#
#
# from typing import Optional, List
#
# from pydantic import BaseModel, Field
#
#
# class UserDto(BaseModel):
#     id: int
#     name: str
#
#
# UserUpdateDto0 = make_optional(UserDto, exclude=['id'])
#
#
# class UserUpdateDto(BaseModel):
#     id: int
#     name: Optional[str] = Field(default=None)
#
#
# class UserUpdateDto(UserDto, metaclass=MakeOptional):
#     class Config:
#         optional_exclude_fields = ['id']
#
#
# #
# print(UserUpdateDto.__fields__)
# # print(UserUpdateDto0.__fields__)
# # print(UserUpdateDto1.__fields__)
#
# UserCreateDto = make_omit(UserDto, ['id'])
# UserDeleteDto = make_omit(UserDto, ['name'])
#
# # class PagingUserDtos(PagingBase):
# #     items: Optional[List[UserDto]]
