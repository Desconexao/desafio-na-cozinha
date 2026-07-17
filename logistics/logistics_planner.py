"""
Módulo de Planejamento de Logística: alocação de pedidos, simulação, gargalos.
Implementação do plano de logística para Módulo 7.
"""

import json
import sys


def load_kitchens(filepath):
    """Carregar kitchens.json e retornar lista de dicts."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo {filepath} não encontrado.")
        return []


def load_orders(filepath):
    """Carregar orders.json e retornar lista de dicts."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo {filepath} não encontrado.")
        return []


def load_regions(filepath):
    """Carregar regions.json e retornar dict {id: region_dict}."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            regions_list = json.load(f)
            return {r['id']: r for r in regions_list}
    except FileNotFoundError:
        print(f"Erro: Arquivo {filepath} não encontrado.")
        return {}


def allocate_orders_greedy(orders, kitchens, graph, regions, recipeBook):
    """
    Allocate orders to kitchens using greedy heuristic.
    
    Algorithm:
    1. For each order (in timestamp order):
    2. Find closest kitchen (Dijkstra) with available capacity in that hour
    3. Assign order to that kitchen; decrement available capacity for that hour
    
    Input:
        orders: list of dicts {id, region_id, recipe_id, timestamp_min}
        kitchens: list of dicts {id, region_id, capacity_per_hour}
        graph: Graph instance for Dijkstra
        regions: dict {id: region_dict}
        recipeBook: RecipeBook instance for recipe metadata
    
    Returns:
        allocation_report: dict
            {
                'allocation': {order_id: kitchen_id},
                'kitchen_loads': {kitchen_id: list of (order_id, recipe_id, timestamp_min)},
                'delayed_orders': [order_ids that couldn't be allocated],
                'gargalos': [kitchen_ids that exceeded capacity]
            }
    """
    from logistics.logistics_algorithms import dijkstra
    
    allocation = {}
    kitchen_loads = {k['id']: [] for k in kitchens}
    delayed_orders = []
    
    # Criar dicionário de capacidade por hora para cada cozinha
    # {kitchen_id: {hour: available_capacity}}
    kitchen_capacity = {}
    for k in kitchens:
        hours = {}
        for hour in range(24):
            hours[hour] = k['capacity_per_hour']
        kitchen_capacity[k['id']] = hours
    
    # Processar pedidos em ordem de timestamp
    sorted_orders = sorted(orders, key=lambda o: o['timestamp_min'])
    
    for order in sorted_orders:
        order_id = order['id']
        order_region = order['region_id']
        timestamp = order['timestamp_min']
        recipe_id = order['recipe_id']
        hour = timestamp // 60
        
        # Encontrar cozinha mais próxima com capacidade
        best_kitchen = None
        best_distance = float('inf')
        
        for kitchen in kitchens:
            kitchen_id = kitchen['id']
            kitchen_region = kitchen['region_id']
            
            # Verificar se cozinha tem capacidade nesta hora
            if kitchen_capacity[kitchen_id].get(hour, 0) > 0:
                # Calcular distância via Dijkstra
                distances, _ = dijkstra(graph, order_region)
                distance = distances.get(kitchen_region, float('inf'))
                
                if distance < best_distance:
                    best_distance = distance
                    best_kitchen = kitchen_id
        
        if best_kitchen:
            allocation[order_id] = best_kitchen
            kitchen_loads[best_kitchen].append((order_id, recipe_id, timestamp))
            kitchen_capacity[best_kitchen][hour] -= 1
        else:
            delayed_orders.append(order_id)
    
    # Identificar gargalos: cozinhas onde total de pedidos > capacity_per_hour * 24
    gargalos = []
    for k in kitchens:
        kitchen_id = k['id']
        total_capacity = k['capacity_per_hour'] * 24
        total_assigned = len(kitchen_loads[kitchen_id])
        
        if total_assigned > total_capacity:
            gargalos.append({
                'kitchen_id': kitchen_id,
                'assigned': total_assigned,
                'capacity': total_capacity,
                'excess': total_assigned - total_capacity
            })
    
    return {
        'allocation': allocation,
        'kitchen_loads': kitchen_loads,
        'delayed_orders': delayed_orders,
        'gargalos': gargalos,
        'kitchen_capacity_remaining': kitchen_capacity
    }


def simulate_logistics(orders, kitchens, graph, regions, recipeBook, horizon_minutes=180):
    """
    Simulate complete logistics: allocation, calculate metrics.
    
    Returns:
        report: dict with throughput, average delivery time, bottlenecks, etc.
    """
    allocation_report = allocate_orders_greedy(orders, kitchens, graph, regions, recipeBook)
    
    allocation = allocation_report['allocation']
    kitchen_loads = allocation_report['kitchen_loads']
    delayed_orders = allocation_report['delayed_orders']
    gargalos = allocation_report['gargalos']
    
    # Calculate statistics
    total_orders = len(orders)
    allocated_orders = len(allocation)
    delivery_times = []
    
    from logistics.logistics_algorithms import dijkstra
    
    for order in orders:
        order_id = order['id']
        if order_id in allocation:
            kitchen_id = allocation[order_id]
            kitchen = next(k for k in kitchens if k['id'] == kitchen_id)
            
            # Tempo de entrega = tempo até cozinha + tempo de preparo
            distances, _ = dijkstra(graph, order['region_id'])
            travel_time = distances.get(kitchen['region_id'], 0)
            
            # Assumir tempo de preparo = recipe.prepTime
            recipe = recipeBook.recipes.get(order['recipe_id'])
            prep_time = recipe.prepTime if recipe else 30  # default 30 min
            
            total_time = travel_time + prep_time
            delivery_times.append(total_time)
    
    avg_delivery_time = sum(delivery_times) / len(delivery_times) if delivery_times else 0
    
    return {
        'total_orders': total_orders,
        'allocated': allocated_orders,
        'delayed': len(delayed_orders),
        'throughput_percent': (allocated_orders / total_orders * 100) if total_orders > 0 else 0,
        'avg_delivery_time_min': avg_delivery_time,
        'kitchen_loads': {k: len(v) for k, v in kitchen_loads.items()},
        'gargalos': gargalos,
        'delayed_order_ids': delayed_orders
    }
