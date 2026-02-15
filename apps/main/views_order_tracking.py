from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from apps.orders.models import Order, OrderItem
from django.db.models import Q
import json
from datetime import datetime

@login_required
def order_tracking_view(request, order_id=None):
    """
    View for tracking order status with real-time updates
    """
    if order_id:
        # Track specific order
        order = get_object_or_404(Order, id=order_id, customer=request.user)
        order_items = OrderItem.objects.filter(order=order)
        
        context = {
            'order': order,
            'order_items': order_items,
            'tracking_active': True
        }
    else:
        # Show all orders for the user
        orders = Order.objects.filter(customer=request.user).order_by('-created_at')
        context = {
            'orders': orders,
            'tracking_active': False
        }
    
    return render(request, 'main/order_tracking.html', context)

@login_required
def order_status_api(request, order_id):
    """
    API endpoint for real-time order status updates
    """
    if request.method == 'GET':
        order = get_object_or_404(Order, id=order_id, customer=request.user)
        
        # Get order items
        order_items = order.items.all()
        
        # Calculate progress percentage
        status_progress = {
            'PENDING': 0,
            'CONFIRMED': 25,
            'PREPARING': 50,
            'READY': 75,
            'COMPLETED': 100,
            'CANCELLED': 0
        }
        
        progress = status_progress.get(order.status, 0)
        
        # Estimated time based on status
        estimated_times = {
            'PENDING': '15-20 mins',
            'CONFIRMED': '12-18 mins',
            'PREPARING': '8-15 mins',
            'READY': '2-5 mins',
            'COMPLETED': 'Completed',
            'CANCELLED': 'Cancelled'
        }
        
        estimated_time = estimated_times.get(order.status, '15-20 mins')
        
        response_data = {
            'status': order.status.lower(),
            'progress': progress,
            'estimated_time': estimated_time,
            'created_at': order.created_at.strftime('%I:%M %p'),
            'updated_at': order.updated_at.strftime('%I:%M %p'),
            'total_amount': float(order.total_amount),
            'table_number': order.table.table_number if order.table else 'N/A',
            'order_items': [
                {
                    'name': item.menu_item.name,
                    'quantity': item.quantity,
                    'price': float(item.price),
                    'subtotal': float(item.subtotal)
                }
                for item in order_items
            ]
        }
        
        return JsonResponse(response_data)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def customer_dashboard_view(request):
    """
    Customer dashboard with order history and profile
    """
    # Get recent orders
    recent_orders = Order.objects.filter(customer=request.user).order_by('-created_at')[:5]
    
    # Calculate statistics
    total_orders = Order.objects.filter(customer=request.user).count()
    total_spent = sum(order.total_amount for order in Order.objects.filter(customer=request.user))
    average_order = total_spent / total_orders if total_orders > 0 else 0
    
    # Get order status counts
    status_counts = {}
    for status in ['PENDING', 'CONFIRMED', 'PREPARING', 'READY', 'COMPLETED', 'CANCELLED']:
        count = Order.objects.filter(customer=request.user, status=status).count()
        if count > 0:
            status_counts[status.lower()] = count
    
    context = {
        'recent_orders': recent_orders,
        'total_orders': total_orders,
        'total_spent': total_spent,
        'average_order': average_order,
        'status_counts': status_counts
    }
    
    return render(request, 'main/customer_dashboard.html', context)
