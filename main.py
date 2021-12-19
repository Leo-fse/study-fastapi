from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, Query

# リクエストボディ
"""
リクエストボディ：クライアントからAPIに送るデータ。
レスポンスボディ：APIからクライアントに送るデータ。
ためにPydanticモデルを使用する。
"""

# リクエストボディを宣言する
class Item(BaseModel):
    """
    モデル属性がデフォルト値を持つ時、必須属性ではなくなる。
    オプショナルな属性にしたいときはNoneを使用する。
    """
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

app = FastAPI()


"""
Pythonの型宣言だけでFast APIは以下のことを実施する。
- リクエストボディをJSONとして受け取ります。
- 適当な型に変換する（必要な場合）
- データを検証します。
    - データが無効な場合は、明確なエラーが返され、どこが不正なデータであったかを示します。
- 受け取ったデータをパラメータ item に変換します。
    - 関数内で Item型であると宣言したので、全ての属性とその型に対するエディタサポート（補完など）を全て使用できます。
- モデルの JSON スキーマ定義を生成し、好きな場所で使用することができます。
- これらのスキーマは、生成されたOpen APIスキーマの一部となり、自動ドキュメントのUIに使用されます。
"""
@app.post("/items1/")
async def create_item(item: Item):
    # 関数内部でモデルの全ての属性に直接アクセスできる。
    item_dict = item.dict()
    price_with_tax = item.price + item.tax
    item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

# リクエストボディ+パスパラメータ
"""
パスパラメータとリクエストボディを同時に宣言できる
FastAPIはパスパラメータである関数パラメータはパスから受け取り、Pydanticモデルによって宣言された関数パラメータはリクエストボディから受け取るということを認識します。

"""
@app.put("/items2/{item_id}")
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}

# リクエストボディ＋パスパラメータ＋クエリパラメータ
"""
また、ボディとパスとクエリのパラメータも同時に宣言できます。
FastAPIはそれぞれを認識し、適切な場所からデータを取得します。
"""
@app.put("/items3/{item_id}")
async def create_item(item_id: int, item: Item, q:Optional[str] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result
"""
関数パラメータは以下のように認識されます。
- パラメータがパスで宣言されている場合は、優先的にパスパラメータとして扱われます。
- パラメータが単数型(int, float, str, bool など)の場合はクエリパラメータとして解釈されます。
- パラメータがPydanticモデル型で宣言された場合、リクエストボディとして解釈されます。
"""

# バリデーション（クエリパラメータと文字列の検証）
"""
1. バリデーションの追加：FastAPIからQueryをインポートする。
from fastapi import Query
2. パラメータのデフォルト値として使用し、パラメータのmax_lengthを50に設定する。
3. min_lemgthも追加する
4. 正規表現を設定する
5. 必須にする場合はQueryの第一引数をNoneから ... に変更する
"""
@app.get("/items4")
async def read_items(q: Optional[str] = Query(..., max_length=50, min_length=3, regex="^fixedquery$")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({q: q})
    return results
