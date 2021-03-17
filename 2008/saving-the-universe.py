
def get_computed_engines(engines, queries):
    # how much engines are found in query
    engines_in_query = {en:0 for en in engines}
    for q in queries:
        engine = engines_in_query.get(q, None)
        if engine is not None:
            engines_in_query[q] = engine + 1

    # reverse key:value
    engines_in_query_reversed = {}
    for key, value in engines_in_query.items():
        engines_in_query_reversed.setdefault(value, [])
        if key not in engines_in_query_reversed[value]:
            engines_in_query_reversed[value].append(key)

    return engines_in_query_reversed

def choose_engines(query, engines, remain_queries):
    zero_found_engine = engines.get(0, [])
    if zero_found_engine:
        # optional engine
        for zero_found in zero_found_engine:
            if zero_found != query:
                return zero_found

    keys = sorted(engines.keys())
    for key in keys:
        for value in engines[key]:
            if value not in remain_queries:
                return value

    position_keys = {}
    for key in keys:
        for value in engines[key]:
            if query != value:
                position_keys[ remain_queries.index(value) ] = value
    if position_keys:
        return position_keys[ max(position_keys.keys()) ]

    raise Exception("could'n found an engine")

def compute_switches(engines, queries, start_with=None):
    switches = 0
    last_engine = start_with
    engines_in_query_reversed = get_computed_engines(engines, queries)
    query_position = -1
    for query in queries:

        query_position += 1
        if last_engine is not None and last_engine != query:
            continue
        engine = choose_engines(query, engines_in_query_reversed, queries[query_position:])
        if last_engine is not None and last_engine != engine:
            switches += 1
        last_engine = engine

    return switches if switches >=0 else 0

def transform_input(text):
    text_gen = (data for data in text.split("\n"))

    read_next = next(text_gen)
    for N in (n for n in range(int(read_next))):
        search_engines = []
        queries = []

        read_next = next(text_gen)
        for engine in (S for S in range(int(read_next))):
            read_next = next(text_gen)
            search_engines.append(read_next)

        read_next = next(text_gen)
        for query in (Q for Q in range(int(read_next))):
            read_next = next(text_gen)
            queries.append(read_next)

        yield search_engines, queries


if __name__ == "__main__":
    t = int(input())
    for i in range(1, t + 1):
        e = int(input())
        engines = [input() for _ in range(e)]
        q = int(input())
        queries = [input() for _ in range(q)]

        results = []
        for start in set(engines):
            results.append( compute_switches(engines, queries, start_with=start) )
        result = 0
        if results:
            result = min(results)

        print("Case #{}: {}".format(i, result))