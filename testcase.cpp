#include <bits/stdc++.h>
using namespace std;

static inline bool has_edge(const vector<vector<int>>& adj, int u, int v) {
	return adj[u][v] != 0 || adj[v][u] != 0;
}

static void dfs_build(int u, const vector<vector<int>>& adj, vector<int>& visited, vector<pair<int, int>>& edges) {
    int n = static_cast<int>(adj.size()) - 1;
    visited[u] = 1;
    for (int v = 1; v <= n; ++v) {
		if (has_edge(adj, u, v) && !visited[v]) {
            edges.push_back({v, u});
            dfs_build(v, adj, visited, edges);
        }
    }
}

int main() {
	if (FILE* f = fopen("CK.INP", "r")) {
		fclose(f);
		FILE* in_file = freopen("CK.INP", "r", stdin);
		FILE* out_file = freopen("CK.OUT", "w", stdout);
		if (!in_file || !out_file) {
			return 0;
		}
	}

	ios::sync_with_stdio(false);
	cin.tie(nullptr);

	int t;
	if (!(cin >> t)) {
		return 0;
	}

	int n, s;
	cin >> n >> s;

	vector<vector<int>> adj(n + 1, vector<int>(n + 1, 0));
	for (int i = 1; i <= n; ++i) {
		for (int j = 1; j <= n; ++j) {
			cin >> adj[i][j];
		}
	}

	vector<pair<int, int>> edges;
	vector<int> visited(n + 1, 0);

	if (t == 1) {
		dfs_build(s, adj, visited, edges);
	} else {
		queue<int> q;
		visited[s] = 1;
		q.push(s);

		while (!q.empty()) {
			int u = q.front();
			q.pop();
			for (int v = 1; v <= n; ++v) {
				if (has_edge(adj, u, v) && !visited[v]) {
					visited[v] = 1;
					edges.push_back({v, u});
					q.push(v);
				}
			}
		}
	}

	if (static_cast<int>(edges.size()) != n - 1) {
		cout << 0 << '\n';
		return 0;
	}

	cout << (n - 1) << '\n';
	for (const auto& e : edges) {
		cout << e.first << ' ' << e.second << '\n';
	}

	return 0;
}
