import typing as tp
from collections import defaultdict
import community as community_louvain
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

from vkapi.friends import get_friends, get_mutual


def ego_network(
    user_id: tp.Optional[int] = None, friends: tp.Optional[tp.List[int]] = None
) -> tp.List[tp.Tuple[int, int]]:
    """
    Построить эгоцентричный граф друзей.

    :param user_id: Идентификатор пользователя, для которого строится граф друзей.
    :param friends: Идентификаторы друзей, между которыми устанавливаются связи.
    """

    result = []
    mutual = get_mutual(user_id, friends)
    print(mutual)
    for each in mutual:
        if len(each) > 1 :
            for friend in each['common_friends']:
                if friend in friends and each['id'] in friends:
                    result.append([each['id'], friend])

    return result


print(ego_network(13589213, [13589213, 1117853, 1554238, 2521999, 3289334, 9616216, 197718955, 4603134]))






def plot_ego_network(net: tp.List[tp.Tuple[int, int]]) -> None:
    graph = nx.Graph()
    graph.add_edges_from(net)
    layout = nx.spring_layout(graph)
    nx.draw(graph, layout, node_size=10, node_color="black", alpha=0.5)
    plt.title("Ego Network", size=15)
    plt.show()


def plot_communities(net: tp.List[tp.Tuple[int, int]]) -> None:
    graph = nx.Graph()
    graph.add_edges_from(net)
    layout = nx.spring_layout(graph)
    partition = community_louvain.best_partition(graph)
    nx.draw(graph, layout, node_size=25, node_color=list(partition.values()), alpha=0.8)
    plt.title("Ego Network", size=15)
    plt.show()


def get_communities(net: tp.List[tp.Tuple[int, int]]) -> tp.Dict[int, tp.List[int]]:
    communities = defaultdict(list)
    graph = nx.Graph()
    graph.add_edges_from(net)
    partition = community_louvain.best_partition(graph)
    for uid, cluster in partition.items():
        communities[cluster].append(uid)
    return communities


def describe_communities(
    clusters: tp.Dict[int, tp.List[int]],
    friends: tp.List[tp.Dict[str, tp.Any]],
    fields: tp.Optional[tp.List[str]] = None,
) -> pd.DataFrame:
    if fields is None:
        fields = ["first_name", "last_name"]

    data = []
    for cluster_n, cluster_users in clusters.items():
        for uid in cluster_users:
            for friend in friends:
                if uid == friend["id"]:
                    data.append([cluster_n] + [friend.get(field) for field in fields])  # type: ignore
                    break
    return pd.DataFrame(data=data, columns=["cluster"] + fields)


print(ego_network(322122))