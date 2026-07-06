#include <stdlib.h>

typedef struct Node {
    struct Node *l;
    struct Node *r;
} Node;

Node* make_tree(int dd) {
    Node* node = (Node*)malloc(sizeof(Node));
    if (node == NULL) return NULL; 
    if (dd > 0) {
        node->l = make_tree(dd - 1);
        node->r = make_tree(dd - 1);
    } else {
        node->l = NULL;
        node->r = NULL;
    }
    return node;
}

int check_tree(Node* node) {
    if (node == NULL) return 0;
    if (node->l == NULL) return 1;
    return 1 + check_tree(node->l) + check_tree(node->r);
}

void free_tree(Node* node) {
    if (node == NULL) return;
    if (node->l != NULL) {
        free_tree(node->l);
        free_tree(node->r);
    }
    free(node);
}

// single-shot execution for transient worker tracking trees
int make_check(int dd) {
    Node* tree = make_tree(dd);
    int result = check_tree(tree);
    free_tree(tree);
    return result;
}