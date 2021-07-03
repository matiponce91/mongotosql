from main import parse_mongodb_query_to_sql


def test_simple_query():
    result = parse_mongodb_query_to_sql("db.user.find({name: 'julio'})")

    assert result == "SELECT * FROM user WHERE name = 'julio'"


def test_lt_operator():
    result = parse_mongodb_query_to_sql("db.user.find({age: {$lt: 13}})")

    assert result == "SELECT * FROM user WHERE age < 13"


def test_lte_operator():
    result = parse_mongodb_query_to_sql("db.user.find({age: {$lte: 13}})")

    assert result == "SELECT * FROM user WHERE age <= 13"


def test_gt_operator():
    result = parse_mongodb_query_to_sql("db.user.find({age: {$gt: 13}})")

    assert result == "SELECT * FROM user WHERE age > 13"


def test_gte_operator():
    result = parse_mongodb_query_to_sql("db.user.find({age: {$gte: 13}})")

    assert result == "SELECT * FROM user WHERE age >= 13"


def test_in_operator():
    result = parse_mongodb_query_to_sql("db.user.find({name:{$in:['appliances','school']}})")

    assert result == "SELECT * FROM user WHERE name IN ('appliances', 'school')"


def test_ne_operator():
    result = parse_mongodb_query_to_sql("db.user.find({name: {$ne: 'pedro'}})")

    assert result == "SELECT * FROM user WHERE name != 'pedro'"


def test_or_operator():
    result = parse_mongodb_query_to_sql("db.user.find({$or: {_id: 23113, name: 'julio'}})")

    assert result == "SELECT * FROM user WHERE _id = 23113 OR name = 'julio'"


def test_and_operator():
    result = parse_mongodb_query_to_sql("db.user.find({$and: {_id: 23113, name: 'julio'}})")

    assert result == "SELECT * FROM user WHERE _id = 23113 AND name = 'julio'"


def test_default_operator():
    result = parse_mongodb_query_to_sql("db.user.find({_id: 23113, name: 'julio'})")

    assert result == "SELECT * FROM user WHERE _id = 23113 AND name = 'julio'"


def test_complex_query():
    result = parse_mongodb_query_to_sql("db.user.find({$or:{_id: 1, name: {$in : ['julio', 'pedro']}}, age: {$ne: 14}}, {_id:1})")

    assert result == "SELECT _id FROM user WHERE _id = 1 OR name IN ('julio', 'pedro') AND age != 14"


def test_from_clause_with_one():
    result = parse_mongodb_query_to_sql("db.user.find({name: 'julio'}, {_id:1})")

    assert result == "SELECT _id FROM user WHERE name = 'julio'"


def test_from_clause_with_zero():
    result = parse_mongodb_query_to_sql("db.user.find({name: 'julio'}, {_id:0})")

    assert result == "SELECT * FROM user WHERE name = 'julio'"


def test_from_clause_with_combined_values():
    result = parse_mongodb_query_to_sql("db.user.find({name: 'julio'}, {_id:0, name: 1})")

    assert result == "SELECT name FROM user WHERE name = 'julio'"


def test_from_clause_not_possible_value():
    result = parse_mongodb_query_to_sql("db.user.find({name: 'julio'}, {_id:2888888})")

    assert result == "SELECT * FROM user WHERE name = 'julio'"


def test_not_accepted_operation(capsys):
    parse_mongodb_query_to_sql("db.user.update({name: 'julio'})")
    out, _ = capsys.readouterr()

    assert out == 'Invalid database method\n'


def test_invalid_clause_initialization(capsys):
    parse_mongodb_query_to_sql("dbdasda.user.update({name: 'julio'})")
    out, _ = capsys.readouterr()

    assert out == 'Invalid clause initialization\n'
