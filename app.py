import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="E-Commerce Analytics",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 E-Commerce Analytics Dashboard")
st.markdown("Complete online shopping analytics — "
            "sales, customers, products and trends.")
st.markdown("---")

# Generate e-commerce dataset
@st.cache_data
def generate_data():
    np.random.seed(42)
    n = 2000

    categories = {
        'Electronics':  {'avg_price': 15000, 'margin': 0.12},
        'Fashion':      {'avg_price': 1500,  'margin': 0.45},
        'Home & Living':{'avg_price': 3000,  'margin': 0.35},
        'Books':        {'avg_price': 400,   'margin': 0.30},
        'Sports':       {'avg_price': 2500,  'margin': 0.38},
        'Beauty':       {'avg_price': 800,   'margin': 0.55},
        'Grocery':      {'avg_price': 500,   'margin': 0.20},
        'Toys':         {'avg_price': 1200,  'margin': 0.40}
    }

    products = {
        'Electronics':   ['Smartphone', 'Laptop',
                          'Earphones', 'Smartwatch',
                          'Tablet', 'Camera'],
        'Fashion':       ['Shirt', 'Jeans',
                          'Dress', 'Shoes',
                          'Kurta', 'Saree'],
        'Home & Living': ['Bedsheet', 'Pillow',
                          'Curtains', 'Lamp',
                          'Wall Art', 'Cookware'],
        'Books':         ['Fiction', 'Self Help',
                          'Technical', 'Comics',
                          'Children', 'Biography'],
        'Sports':        ['Cricket Bat', 'Football',
                          'Yoga Mat', 'Dumbbells',
                          'Cycling', 'Swimming'],
        'Beauty':        ['Moisturizer', 'Lipstick',
                          'Shampoo', 'Perfume',
                          'Face Wash', 'Sunscreen'],
        'Grocery':       ['Rice', 'Dal',
                          'Oil', 'Spices',
                          'Snacks', 'Beverages'],
        'Toys':          ['Board Game', 'LEGO',
                          'Remote Car', 'Doll',
                          'Puzzle', 'Action Figure']
    }

    cities = {
        'Mumbai':     0.18, 'Delhi':      0.16,
        'Bangalore':  0.14, 'Hyderabad':  0.10,
        'Pune':       0.08, 'Chennai':    0.08,
        'Kolkata':    0.07, 'Ahmedabad':  0.06,
        'Jaipur':     0.05, 'Bhubaneswar':0.03,
        'Others':     0.05
    }

    payment_methods = {
        'UPI':         0.45,
        'Credit Card': 0.20,
        'Debit Card':  0.15,
        'COD':         0.15,
        'Net Banking': 0.05
    }

    start_date = datetime(2023, 1, 1)
    rows       = []

    for i in range(n):
        cat      = np.random.choice(
            list(categories.keys()))
        product  = np.random.choice(
            products[cat])
        cat_cfg  = categories[cat]

        base_price = cat_cfg['avg_price']
        price      = base_price * \
            np.random.uniform(0.5, 2.0)
        qty        = np.random.randint(1, 5)
        discount   = np.random.choice(
            [0, 5, 10, 15, 20, 30, 40, 50],
            p=[0.3, 0.15, 0.15, 0.1,
               0.1, 0.08, 0.07, 0.05])
        final_price = price * (1 - discount/100)
        revenue     = final_price * qty
        profit      = revenue * cat_cfg['margin']

        days_offset = np.random.randint(0, 365)
        order_date  = start_date + \
            timedelta(days=days_offset)

        city    = np.random.choice(
            list(cities.keys()),
            p=list(cities.values()))
        payment = np.random.choice(
            list(payment_methods.keys()),
            p=list(payment_methods.values()))
        rating  = np.random.choice(
            [1, 2, 3, 4, 5],
            p=[0.05, 0.08, 0.15, 0.35, 0.37])
        returned = np.random.choice(
            [True, False],
            p=[0.08, 0.92])
        delivery_days = np.random.randint(1, 8)

        rows.append({
            'order_id':      f"ORD{i+1:05d}",
            'product':       product,
            'category':      cat,
            'price':         round(price, 2),
            'qty':           qty,
            'discount':      discount,
            'final_price':   round(final_price, 2),
            'revenue':       round(revenue, 2),
            'profit':        round(profit, 2),
            'order_date':    order_date,
            'month':         order_date.month,
            'quarter':       (order_date.month-1)
                             //3 + 1,
            'day_name':      order_date\
                             .strftime('%A'),
            'city':          city,
            'payment':       payment,
            'rating':        rating,
            'returned':      returned,
            'delivery_days': delivery_days,
            'customer_id':   f"CUS{np.random.randint(1, 501):04d}"
        })

    return pd.DataFrame(rows)

df = generate_data()

# Sidebar
st.sidebar.header("🔍 Filters")
cat_filter = st.sidebar.multiselect(
    "Category:",
    df['category'].unique(),
    default=df['category'].unique()
)
city_filter = st.sidebar.multiselect(
    "City:",
    df['city'].unique(),
    default=df['city'].unique()
)
month_filter = st.sidebar.multiselect(
    "Month:",
    sorted(df['month'].unique()),
    default=sorted(df['month'].unique())
)

filtered = df[
    (df['category'].isin(cat_filter)) &
    (df['city'].isin(city_filter)) &
    (df['month'].isin(month_filter))
].copy()

month_names = ['Jan','Feb','Mar','Apr',
               'May','Jun','Jul','Aug',
               'Sep','Oct','Nov','Dec']

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Overview",
    "📈 Sales Trends",
    "🏆 Products",
    "👥 Customers",
    "🚚 Operations",
    "💰 Profitability"
])

# Tab 1 — Overview
with tab1:
    st.markdown("### 📊 Business KPIs")

    total_rev    = filtered['revenue'].sum()
    total_orders = len(filtered)
    total_profit = filtered['profit'].sum()
    avg_order    = filtered['revenue'].mean()
    return_rate  = filtered['returned'].mean()
    avg_rating   = filtered['rating'].mean()

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Revenue",
              f"₹{total_rev/1e7:.2f}Cr")
    c2.metric("Orders",
              f"{total_orders:,}")
    c3.metric("Profit",
              f"₹{total_profit/1e6:.1f}L")
    c4.metric("Avg Order",
              f"₹{avg_order:,.0f}")
    c5.metric("Return Rate",
              f"{return_rate:.1%}")
    c6.metric("Avg Rating",
              f"{avg_rating:.2f} ⭐")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        monthly = filtered.groupby(
            'month')['revenue'].sum()
        monthly_df = pd.DataFrame({
            'month': [month_names[m-1]
                      for m in monthly.index],
            'revenue': monthly.values
        })
        fig = px.bar(
            monthly_df,
            x='month', y='revenue',
            title='Monthly Revenue (₹)',
            color='revenue',
            color_continuous_scale='Blues'
        )
        fig.update_layout(
            height=350,
            template='plotly_white'
        )
        st.plotly_chart(fig,
                        use_container_width=True)

    with col2:
        cat_rev = filtered.groupby(
            'category')['revenue'].sum()
        fig2 = px.pie(
            values=cat_rev.values,
            names=cat_rev.index,
            title='Revenue by Category',
            color_discrete_sequence=
                px.colors.qualitative.Set3
        )
        fig2.update_layout(height=350)
        st.plotly_chart(fig2,
                        use_container_width=True)

# Tab 2 — Sales Trends
with tab2:
    st.markdown("### 📈 Sales Trends")

    col1, col2 = st.columns(2)

    with col1:
        # Day of week
        dow_order = ['Monday', 'Tuesday',
                     'Wednesday', 'Thursday',
                     'Friday', 'Saturday',
                     'Sunday']
        dow_sales = filtered.groupby(
            'day_name')['revenue'].mean()
        dow_sales = dow_sales.reindex(
            [d for d in dow_order
             if d in dow_sales.index])

        fig3 = px.bar(
            x=dow_sales.index,
            y=dow_sales.values,
            title='Avg Revenue by Day of Week',
            color=dow_sales.values,
            color_continuous_scale='Purples'
        )
        fig3.update_layout(
            height=350,
            template='plotly_white',
            yaxis_title='Avg Revenue (₹)'
        )
        st.plotly_chart(fig3,
                        use_container_width=True)

    with col2:
        # Discount vs Revenue
        disc_rev = filtered.groupby(
            'discount')['revenue'].mean()
        fig4 = px.line(
            x=disc_rev.index,
            y=disc_rev.values,
            title='Avg Revenue by Discount %',
            markers=True,
            color_discrete_sequence=['#e74c3c']
        )
        fig4.update_layout(
            height=350,
            template='plotly_white',
            xaxis_title='Discount %',
            yaxis_title='Avg Revenue (₹)'
        )
        st.plotly_chart(fig4,
                        use_container_width=True)

    # Payment methods
    col3, col4 = st.columns(2)

    with col3:
        pay_counts = filtered[
            'payment'].value_counts()
        fig5 = px.pie(
            values=pay_counts.values,
            names=pay_counts.index,
            title='Payment Methods',
            color_discrete_sequence=
                px.colors.qualitative.Pastel
        )
        fig5.update_layout(height=350)
        st.plotly_chart(fig5,
                        use_container_width=True)

    with col4:
        # City sales
        city_rev = filtered.groupby(
            'city')['revenue'].sum()\
            .sort_values(ascending=False)
        fig6 = px.bar(
            x=city_rev.index,
            y=city_rev.values / 1e5,
            title='Revenue by City (₹ Lakhs)',
            color=city_rev.values,
            color_continuous_scale='Oranges'
        )
        fig6.update_layout(
            height=350,
            template='plotly_white',
            yaxis_title='Revenue (₹L)'
        )
        fig6.update_xaxes(tickangle=45)
        st.plotly_chart(fig6,
                        use_container_width=True)

# Tab 3 — Products
with tab3:
    st.markdown("### 🏆 Product Analytics")

    col1, col2 = st.columns(2)

    with col1:
        top_products = filtered.groupby(
            'product')['revenue'].sum()\
            .sort_values(ascending=False)\
            .head(15)
        fig7 = px.bar(
            x=top_products.values / 1e5,
            y=top_products.index,
            orientation='h',
            title='Top 15 Products by Revenue',
            color=top_products.values,
            color_continuous_scale='Viridis'
        )
        fig7.update_layout(
            height=500,
            template='plotly_white',
            xaxis_title='Revenue (₹L)'
        )
        st.plotly_chart(fig7,
                        use_container_width=True)

    with col2:
        # Rating distribution
        prod_rating = filtered.groupby(
            'category').agg(
            avg_rating=('rating', 'mean'),
            orders=('order_id', 'count')
        ).reset_index()

        fig8 = px.scatter(
            prod_rating,
            x='avg_rating',
            y='orders',
            size='orders',
            color='category',
            title='Category Rating vs Orders',
            labels={
                'avg_rating': 'Avg Rating',
                'orders': 'Total Orders'
            }
        )
        fig8.update_layout(
            height=500,
            template='plotly_white'
        )
        st.plotly_chart(fig8,
                        use_container_width=True)

    # Return rates by category
    st.markdown(
        "#### 📦 Return Rate by Category")
    cat_returns = filtered.groupby(
        'category')['returned'].mean()\
        .sort_values(ascending=False)

    fig9 = px.bar(
        x=cat_returns.index,
        y=cat_returns.values * 100,
        title='Return Rate by Category (%)',
        color=cat_returns.values,
        color_continuous_scale='Reds'
    )
    fig9.update_layout(
        height=300,
        template='plotly_white',
        yaxis_title='Return Rate (%)'
    )
    st.plotly_chart(fig9,
                    use_container_width=True)

# Tab 4 — Customers
with tab4:
    st.markdown("### 👥 Customer Analytics")

    # Customer segments by order value
    cust_stats = filtered.groupby(
        'customer_id').agg(
        total_spent=('revenue', 'sum'),
        orders=('order_id', 'count'),
        avg_rating=('rating', 'mean'),
        returns=('returned', 'sum')
    ).reset_index()

    # RFM-style segmentation
    cust_stats['segment'] = pd.cut(
        cust_stats['total_spent'],
        bins=[0, 5000, 20000,
              50000, float('inf')],
        labels=['Bronze', 'Silver',
                'Gold', 'Platinum']
    )

    col1, col2 = st.columns(2)

    with col1:
        seg_counts = cust_stats[
            'segment'].value_counts()
        seg_colors = {
            'Platinum': '#9b59b6',
            'Gold':     '#f39c12',
            'Silver':   '#95a5a6',
            'Bronze':   '#cd6133'
        }
        fig10 = px.pie(
            values=seg_counts.values,
            names=seg_counts.index,
            title='Customer Segments',
            color=seg_counts.index,
            color_discrete_map=seg_colors
        )
        fig10.update_layout(height=400)
        st.plotly_chart(fig10,
                        use_container_width=True)

    with col2:
        fig11 = px.scatter(
            cust_stats,
            x='orders',
            y='total_spent',
            color='segment',
            title='Orders vs Total Spent',
            color_discrete_map=seg_colors,
            labels={
                'orders': 'Number of Orders',
                'total_spent': 'Total Spent (₹)'
            }
        )
        fig11.update_layout(
            height=400,
            template='plotly_white'
        )
        st.plotly_chart(fig11,
                        use_container_width=True)

    # Segment stats
    seg_stats = cust_stats.groupby(
        'segment', observed=True).agg(
        customers=('customer_id', 'count'),
        avg_spent=('total_spent', 'mean'),
        avg_orders=('orders', 'mean')
    ).reset_index()

    seg_stats['avg_spent'] = \
        seg_stats['avg_spent'].apply(
            lambda x: f"₹{x:,.0f}")
    seg_stats['avg_orders'] = \
        seg_stats['avg_orders'].round(1)
    seg_stats.columns = [
        'Segment', 'Customers',
        'Avg Spent', 'Avg Orders'
    ]
    st.dataframe(seg_stats,
                 use_container_width=True,
                 hide_index=True)

# Tab 5 — Operations
with tab5:
    st.markdown("### 🚚 Operational Analytics")

    col1, col2 = st.columns(2)

    with col1:
        # Delivery days distribution
        fig12 = px.histogram(
            filtered,
            x='delivery_days',
            nbins=7,
            title='Delivery Time Distribution',
            color_discrete_sequence=['#3498db']
        )
        fig12.update_layout(
            height=350,
            template='plotly_white',
            xaxis_title='Delivery Days',
            yaxis_title='Orders'
        )
        st.plotly_chart(fig12,
                        use_container_width=True)

    with col2:
        # Rating by delivery time
        del_rating = filtered.groupby(
            'delivery_days')['rating'].mean()
        fig13 = px.line(
            x=del_rating.index,
            y=del_rating.values,
            title='Rating vs Delivery Days',
            markers=True,
            color_discrete_sequence=['#e74c3c']
        )
        fig13.update_layout(
            height=350,
            template='plotly_white',
            xaxis_title='Delivery Days',
            yaxis_title='Avg Rating'
        )
        st.plotly_chart(fig13,
                        use_container_width=True)

    # Ops metrics
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Avg Delivery",
              f"{filtered['delivery_days'].mean():.1f} days")
    s2.metric("Same Day (1 day)",
              f"{(filtered['delivery_days']==1).mean():.1%}")
    s3.metric("Returns",
              f"{filtered['returned'].sum():,}")
    s4.metric("Avg Rating",
              f"{filtered['rating'].mean():.2f} ⭐")

    # Category delivery heatmap
    del_cat = filtered.groupby(
        ['category', 'delivery_days']
    ).size().unstack(fill_value=0)

    fig14 = px.imshow(
        del_cat,
        title='Orders: Category × Delivery Days',
        color_continuous_scale='Blues',
        labels=dict(color='Orders')
    )
    fig14.update_layout(
        height=400,
        template='plotly_white'
    )
    st.plotly_chart(fig14,
                    use_container_width=True)

# Tab 6 — Profitability
with tab6:
    st.markdown("### 💰 Profitability Analysis")

    col1, col2 = st.columns(2)

    with col1:
        cat_profit = filtered.groupby(
            'category').agg(
            revenue=('revenue', 'sum'),
            profit=('profit', 'sum')
        ).reset_index()
        cat_profit['margin'] = (
            cat_profit['profit'] /
            cat_profit['revenue'] * 100
        ).round(1)

        fig15 = px.bar(
            cat_profit.sort_values(
                'margin', ascending=False),
            x='category', y='margin',
            title='Profit Margin by Category (%)',
            color='margin',
            color_continuous_scale='RdYlGn'
        )
        fig15.update_layout(
            height=350,
            template='plotly_white',
            yaxis_title='Margin (%)'
        )
        fig15.update_xaxes(tickangle=45)
        st.plotly_chart(fig15,
                        use_container_width=True)

    with col2:
        fig16 = px.scatter(
            cat_profit,
            x='revenue', y='profit',
            size='margin',
            color='category',
            title='Revenue vs Profit by Category',
            text='category',
            labels={
                'revenue': 'Revenue (₹)',
                'profit': 'Profit (₹)'
            }
        )
        fig16.update_traces(
            textposition='top center',
            textfont_size=9)
        fig16.update_layout(
            height=350,
            template='plotly_white'
        )
        st.plotly_chart(fig16,
                        use_container_width=True)

    # Profit table
    profit_table = cat_profit.copy()
    profit_table['revenue'] = \
        profit_table['revenue'].apply(
            lambda x: f"₹{x/1e5:.1f}L")
    profit_table['profit'] = \
        profit_table['profit'].apply(
            lambda x: f"₹{x/1e5:.1f}L")
    profit_table['margin'] = \
        profit_table['margin'].apply(
            lambda x: f"{x:.1f}%")
    profit_table.columns = [
        'Category', 'Revenue',
        'Profit', 'Margin %'
    ]
    st.dataframe(profit_table,
                 use_container_width=True,
                 hide_index=True)

    # Download
    csv = filtered.to_csv(index=False)
    st.download_button(
        "⬇️ Download Order Data",
        csv, "ecommerce_data.csv",
        "text/csv"
    )

st.markdown("---")
st.markdown(
    "Built by **Jyotiraditya** | "
    "E-Commerce Analytics Dashboard | "
    "2000 orders analyzed"
)