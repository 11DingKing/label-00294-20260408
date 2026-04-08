<template>
  <div class="page-container">
    <div class="filter-bar">
      <div class="filter-left">
        <el-radio-group v-model="timeRange" @change="handleTimeRangeChange">
          <el-radio-button label="all">全部</el-radio-button>
          <el-radio-button label="week">本周</el-radio-button>
          <el-radio-button label="month">本月</el-radio-button>
          <el-radio-button label="custom">自定义</el-radio-button>
        </el-radio-group>
        
        <el-date-picker
          v-if="timeRange === 'custom'"
          v-model="dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          value-format="YYYY-MM-DD"
          class="date-picker"
          @change="handleDateRangeChange"
        />
      </div>
      
      <div class="filter-right">
        <el-button type="primary" @click="loadStatistics">
          <el-icon><Refresh /></el-icon>
          刷新数据
        </el-button>
      </div>
    </div>

    <div class="stats-row">
      <div class="stat-card">
        <div class="stat-icon total">
          <el-icon><Document /></el-icon>
        </div>
        <div class="stat-content">
          <span class="stat-value">{{ statistics.summary?.total_orders || 0 }}</span>
          <span class="stat-label">订单总数</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon amount">
          <el-icon><Money /></el-icon>
        </div>
        <div class="stat-content">
          <span class="stat-value">¥{{ (statistics.summary?.total_amount || 0).toFixed(2) }}</span>
          <span class="stat-label">总金额</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon pending">
          <el-icon><Clock /></el-icon>
        </div>
        <div class="stat-content">
          <span class="stat-value">{{ statistics.summary?.pending_count || 0 }}</span>
          <span class="stat-label">待处理</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon completed">
          <el-icon><CircleCheck /></el-icon>
        </div>
        <div class="stat-content">
          <span class="stat-value">{{ statistics.summary?.completed_count || 0 }}</span>
          <span class="stat-label">已完成</span>
        </div>
      </div>
    </div>

    <div class="charts-grid">
      <div class="chart-card">
        <div class="chart-header">
          <h3 class="chart-title">各状态订单数量</h3>
        </div>
        <div class="chart-body">
          <v-chart 
            v-if="statusChartOption" 
            :option="statusChartOption" 
            autoresize 
            class="chart"
          />
          <div v-else class="empty-chart">
            <el-icon :size="48"><PieChart /></el-icon>
            <p>暂无数据</p>
          </div>
        </div>
      </div>

      <div class="chart-card">
        <div class="chart-header">
          <h3 class="chart-title">订单来源分布</h3>
        </div>
        <div class="chart-body">
          <v-chart 
            v-if="sourceChartOption" 
            :option="sourceChartOption" 
            autoresize 
            class="chart"
          />
          <div v-else class="empty-chart">
            <el-icon :size="48"><PieChart /></el-icon>
            <p>暂无数据</p>
          </div>
        </div>
      </div>

      <div class="chart-card full-width">
        <div class="chart-header">
          <h3 class="chart-title">每月订单金额趋势</h3>
        </div>
        <div class="chart-body">
          <v-chart 
            v-if="trendChartOption" 
            :option="trendChartOption" 
            autoresize 
            class="chart"
          />
          <div v-else class="empty-chart">
            <el-icon :size="48"><TrendCharts /></el-icon>
            <p>暂无数据</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref, computed } from 'vue'
import { getStatistics } from '@/api/orders'
import { toast } from '@/utils/toast'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, LineChart, PieChart as EPieChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DatasetComponent,
  TransformComponent
} from 'echarts/components'
import VChart from 'vue-echarts'
import {
  Refresh, Document, Money, Clock, CircleCheck,
  PieChart, TrendCharts
} from '@element-plus/icons-vue'

use([
  CanvasRenderer,
  BarChart,
  LineChart,
  EPieChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DatasetComponent,
  TransformComponent
])

const loading = ref(false)
const timeRange = ref('all')
const dateRange = ref(null)

const statistics = reactive({
  summary: null,
  status_stats: [],
  monthly_trend: [],
  source_distribution: []
})

const statusChartOption = computed(() => {
  if (!statistics.status_stats || statistics.status_stats.length === 0) {
    return null
  }
  
  const statusColors = {
    'pending': '#f59e0b',
    'processing': '#3b82f6',
    'shipped': '#6366f1',
    'delivered': '#10b981',
    'cancelled': '#ef4444'
  }
  
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: statistics.status_stats.map(s => s.status_display),
      axisLabel: {
        interval: 0,
        rotate: 0
      }
    },
    yAxis: {
      type: 'value',
      minInterval: 1
    },
    series: [
      {
        name: '订单数量',
        type: 'bar',
        barWidth: '50%',
        data: statistics.status_stats.map((s, index) => ({
          value: s.count,
          itemStyle: {
            color: statusColors[s.status] || '#6366f1',
            borderRadius: [8, 8, 0, 0]
          }
        })),
        label: {
          show: true,
          position: 'top',
          fontWeight: 'bold'
        }
      }
    ]
  }
})

const trendChartOption = computed(() => {
  if (!statistics.monthly_trend || statistics.monthly_trend.length === 0) {
    return null
  }
  
  return {
    tooltip: {
      trigger: 'axis',
      formatter: (params) => {
        const data = params[0]
        return `${data.name}<br/>订单金额: ¥${data.value.toFixed(2)}`
      }
    },
    legend: {
      data: ['订单金额'],
      bottom: 0
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      top: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: statistics.monthly_trend.map(t => t.month)
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        formatter: '¥{value}'
      }
    },
    series: [
      {
        name: '订单金额',
        type: 'line',
        smooth: true,
        symbol: 'circle',
        symbolSize: 8,
        lineStyle: {
          width: 3,
          color: '#6366f1'
        },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(99, 102, 241, 0.3)' },
              { offset: 1, color: 'rgba(99, 102, 241, 0.05)' }
            ]
          }
        },
        itemStyle: {
          color: '#6366f1'
        },
        data: statistics.monthly_trend.map(t => t.total_amount)
      }
    ]
  }
})

const sourceChartOption = computed(() => {
  if (!statistics.source_distribution || statistics.source_distribution.length === 0) {
    return null
  }
  
  const colors = ['#6366f1', '#3b82f6', '#10b981', '#f59e0b', '#ef4444']
  
  return {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: '5%',
      top: 'center'
    },
    series: [
      {
        name: '订单来源',
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['35%', '50%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: statistics.source_distribution.map((s, index) => ({
          name: s.name,
          value: s.value,
          itemStyle: {
            color: colors[index % colors.length]
          }
        }))
      }
    ]
  }
})

const loadStatistics = async () => {
  loading.value = true
  try {
    const params = {}
    
    if (timeRange.value === 'custom' && dateRange.value && dateRange.value.length === 2) {
      params.time_range = 'custom'
      params.start_date = dateRange.value[0]
      params.end_date = dateRange.value[1]
    } else if (timeRange.value !== 'all') {
      params.time_range = timeRange.value
    }
    
    const response = await getStatistics(params)
    
    if (response.code === 200) {
      const data = response.data
      statistics.summary = data.summary
      statistics.status_stats = data.status_stats
      statistics.monthly_trend = data.monthly_trend
      statistics.source_distribution = data.source_distribution
    } else {
      toast.error(response.message || '获取统计数据失败')
    }
  } catch (error) {
    toast.error('获取统计数据失败')
  } finally {
    loading.value = false
  }
}

const handleTimeRangeChange = () => {
  if (timeRange.value !== 'custom') {
    dateRange.value = null
  }
  loadStatistics()
}

const handleDateRangeChange = () => {
  if (dateRange.value && dateRange.value.length === 2) {
    loadStatistics()
  }
}

onMounted(() => {
  loadStatistics()
})
</script>

<style scoped lang="scss">
.page-container {
  padding: 24px;
}

.filter-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 16px 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  
  .filter-left {
    display: flex;
    align-items: center;
    gap: 16px;
  }
  
  .date-picker {
    width: 280px;
  }
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  }
  
  .stat-icon {
    width: 56px;
    height: 56px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    
    &.total {
      background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%);
      color: #4f46e5;
    }
    
    &.amount {
      background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
      color: #059669;
    }
    
    &.pending {
      background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
      color: #d97706;
    }
    
    &.completed {
      background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
      color: #2563eb;
    }
  }
  
  .stat-content {
    display: flex;
    flex-direction: column;
    
    .stat-value {
      font-size: 28px;
      font-weight: 700;
      color: #1f2937;
      line-height: 1;
    }
    
    .stat-label {
      font-size: 14px;
      color: #6b7280;
      margin-top: 4px;
    }
  }
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
  
  .full-width {
    grid-column: 1 / -1;
  }
}

.chart-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  
  .chart-header {
    padding: 20px 24px;
    border-bottom: 1px solid #f3f4f6;
    
    .chart-title {
      margin: 0;
      font-size: 16px;
      font-weight: 600;
      color: #1f2937;
    }
  }
  
  .chart-body {
    padding: 20px;
    min-height: 320px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .chart {
    width: 100%;
    height: 300px;
  }
  
  .empty-chart {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: #9ca3af;
    
    p {
      margin-top: 12px;
      font-size: 14px;
    }
  }
}

@media (max-width: 1200px) {
  .stats-row {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .charts-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .stats-row {
    grid-template-columns: 1fr;
  }
  
  .filter-bar {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
    
    .filter-left {
      flex-wrap: wrap;
    }
  }
}
</style>
