from collections import defaultdict

class FPNode:
    def _init_(self, item, count, parent):
        self.item = item
        self.count = count
        self.parent = parent
        self.children = defaultdict()
        self.node_link = None

def create_fptree(transactions, min_support):
    header_table = defaultdict(int)
    for transaction in transactions:
        for item in transaction:
            header_table[item] += 1
    header_table = {k: v for k, v in header_table.items() if v >= min_support}
    frequent_items = set(header_table.keys())

    if len(frequent_items) == 0:
        return None, None

    for k in header_table:
        header_table[k] = [header_table[k], None]

    root = FPNode()

    for transaction in transactions:
        transaction = [item for item in transaction if item in frequent_items]
        transaction.sort(key=lambda item: header_table[item][0], reverse=True)
        current_node = root
        for item in transaction:
            current_node = insert_node(item, current_node, header_table)
    
    return root, header_table

def insert_node(item, node, header_table):
    if item in node.children:
        node.children[item].count += 1
    else:
        new_node = FPNode(item, 1, node)
        node.children[item] = new_node
        if header_table[item][1] is None:
            header_table[item][1] = new_node
        else:
            update_header(header_table[item][1], new_node)
    return node.children[item]

def update_header(node_to_test, target_node):
    while node_to_test.node_link is not None:
        node_to_test = node_to_test.node_link
    node_to_test.node_link = target_node

def ascend_tree(node):
    path = []
    while node.parent is not None:
        path.append(node.item)
        node = node.parent
    return path

def find_frequent_itemsets(header_table, prefix, frequent_itemsets, min_support):
    sorted_items = sorted(header_table.items(), key=lambda item: item[1][0])
    for item, data in sorted_items:
        support = data[0]
        if support >= min_support and item not in prefix:
            frequent_itemset = prefix + [item]
            frequent_itemsets.append((frequent_itemset, support))
            cond_pattern_base = []
            node = data[1]
            while node is not None:
                path = ascend_tree(node)
                if len(path) > 1:
                    cond_pattern_base.append(path[1:])
                node = node.node_link
            cond_tree, cond_header_table = create_fptree(cond_pattern_base, min_support)
            if cond_header_table is not None:
                find_frequent_itemsets(cond_header_table, frequent_itemset, frequent_itemsets, min_support)

def fpgrowth(transactions, min_support):
    root, header_table = create_fptree(transactions, min_support)
    frequent_itemsets = []
    find_frequent_itemsets(header_table, [], frequent_itemsets, min_support)
    return frequent_itemsets

# Sample transaction data
transactions = [['milk', 'bread', 'butter'],
                ['milk', 'bread', 'jam'],
                ['milk', 'butter'],
                ['bread', 'jam'],
                ['bread', 'butter'],
                ['milk', 'bread', 'butter', 'jam'],
                ['bread', 'butter', 'jam']]

# Apply FP-Growth algorithm
frequent_itemsets = fpgrowth(transactions, min_support=3)

# for itemset, support in frequent_itemsets:
    # print(itemset, support)