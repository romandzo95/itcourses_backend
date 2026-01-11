from django.shortcuts import render
from .serializers import *
from django.db.models import Count, Avg, Sum, F
from django.db.models.functions import ExtractMonth
from django.views import View
import pandas as pd

import plotly.io as pio
import plotly.express as px
from django.shortcuts import render

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.embed import components
from math import pi
from bokeh.transform import cumsum, linear_cmap
from bokeh.palettes import Spectral6, Viridis256, Turbo256
from bokeh.resources import CDN
from .parallel_db import benchmark

from .queries import *
# Create your views here.

class PlotlyDashboardView(View):
    def get(self, request):
        
        #=========== 1 =============
        min_courses = int(request.GET.get('min_courses', 1))
        
        df_enrollments = get_student_enrollments()
        df_enrollments = df_enrollments[df_enrollments["total_courses"] >= min_courses]


        if not df_enrollments.empty:
            df_enrollments['full_name'] = df_enrollments['first_name']+' '+df_enrollments['last_name']
            fig1 = px.bar(df_enrollments, x='full_name', y='total_courses', title="Students enrolled on courses")
        else:
            fig1 = px.bar(title="No data")
        chart1 = pio.to_html(fig1, full_html=False)

        #=========== 2 =============
        min_grade = float(request.GET.get('min_grade', 6.0))
        df_grades = get_student_avg_grade()
        df_grades = df_grades[df_grades["avg_grade"] >= min_grade]

        if not df_grades.empty:
            df_grades['avg_grade'] = df_grades['avg_grade'].astype(float)
            df_grades['full_name'] = df_grades['first_name'] + " " + df_grades['last_name']
            fig2 = px.scatter(df_grades, x='full_name', y='avg_grade', size='avg_grade', color='avg_grade', title="Student`s grades")
        else:
            fig2 = px.scatter(title="No data")
        chart2 = pio.to_html(fig2, full_html=False)

        #=========== 3 =============
        df_profit = get_course_profit()[["course_name", "total_income"]]

        if not df_profit.empty:
            fig3 = px.pie(df_profit, values='total_income', names='course_name', title="Course profits")
        else:
            fig3 = px.pie(title="No data")
        chart3 = pio.to_html(fig3, full_html=False)

        #=========== 4 =============
        df_classrooms = get_classroom_availability()[["room_number", "lessons_count"]]

        if not df_classrooms.empty:
            fig4 = px.bar(df_classrooms, x='lessons_count', y='room_number', orientation='h', title="Classrooms availability")
        else:
            fig4 = px.bar(title="No data")
        chart4 = pio.to_html(fig4, full_html=False)

        #=========== 5 =============
        df_payments = get_payments_by_method()

        if not df_payments.empty:
            fig5 = px.pie(df_payments, values='total', names='method', hole=0.4, title="Payment methods")
        else:
            fig5 = px.pie(title="No data")
        chart5 = pio.to_html(fig5, full_html=False)

        #=========== 6 =============
        df_income = get_monthly_income()

        if not df_income.empty:
            fig6 = px.line(df_income,x='month', y='monthly_income', markers=True, title="Monthly profit")
        else:
            fig6 = px.line(title="No data")
        chart6 = pio.to_html(fig6, full_html=False)


        context = {
            'chart1': chart1, 'chart2': chart2, 'chart3': chart3,
            'chart4': chart4, 'chart5': chart5, 'chart6': chart6,
            'min_courses': min_courses,
            'min_grade': min_grade
        }
        return render(request, 'itcourses_ui/dashboard_plotly.html', context)





class BokehDashboardView(View):
    def get(self, request):
        try:
            min_courses = int(request.GET.get('min_courses', 1))
        except ValueError:
            min_courses = 1
            
        try:
            min_grade = float(request.GET.get('min_grade', 6.0))
        except ValueError:
            min_grade = 6.0

        plots = {}

        # =========== 1 ==============
        df1 = get_student_enrollments()
        df1 = df1[df1["total_courses"] >= min_courses]

        if not df1.empty:
            df1['full_name'] = df1['first_name'] + ' ' + df1['last_name']
            df1 = df1.drop_duplicates(subset=['full_name'])
            source1 = ColumnDataSource(df1)
            names = df1['full_name'].tolist()
            p1 = figure(x_range=names, height=350, title="Students enrolled on courses",
                        toolbar_location=None, tools="")
            p1.vbar(x='full_name', top='total_courses', width=0.9, source=source1, 
                    line_color='white', fill_color="#718dbf")
            p1.add_tools(HoverTool(tooltips=[("Student", "@full_name"), ("Courses", "@total_courses")]))
            p1.xaxis.major_label_orientation = 1.0
            plots['chart1'] = p1
        else:
            p1 = figure(title="No Data")
            plots['chart1'] = p1

        
        # =========== 2 =============

        df2 = get_student_avg_grade()
        df2 = df2[df2["avg_grade"] >= min_grade]

        if not df2.empty:
            df2['avg_grade'] = df2['avg_grade'].astype(float)
            df2['full_name'] = df2['first_name'] + " " + df2['last_name']

            df2 = df2.drop_duplicates(subset=['full_name'])

            df2['size']=df2["avg_grade"]*1.5
            source2 = ColumnDataSource(df2)
            names = df2['full_name'].tolist()
            mapper = linear_cmap(field_name='avg_grade', 
                                 palette=Viridis256, 
                                 low=df2["avg_grade"].min(),
                                 high=df2['avg_grade'].max())
            p2 = figure(x_range=names, height=350, title="Student`s Grades")
            p2.circle(x='full_name', y='avg_grade', size='size', source=source2,
                       line_color=mapper,fill_color=mapper,
                       fill_alpha=0.6)
            p2.xaxis.major_label_orientation = 1.2
            p2.add_tools(HoverTool(tooltips=[("Name", "@full_name"), ("Grade", "@avg_grade")]))
            plots['chart2'] = p2
            
        else:
            p2 = figure(title="No Data")
            plots['chart2'] = p2

        # =========== 3 =============

        df3 = get_course_profit()


        if not df3.empty:
            df3['total_income'] = df3['total_income'].astype(float)
            df3['angle'] = df3['total_income'] / df3['total_income'].sum() * 2 * pi
            df3['color'] = [Spectral6[i % 6] for i in range(len(df3))]

            source3 = ColumnDataSource(df3)

            p3 = figure(height=350, title="Course Profits", toolbar_location=None,
                        tools="hover", tooltips="@course_name: @total_income", x_range=(-0.5, 1.0))
            
            p3.wedge(x=0, y=1, radius=0.4,
                     start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                     line_color="white", fill_color='color', legend_field='course_name', source=source3)
            
            p3.axis.visible = False
            p3.grid.grid_line_color = None
            plots['chart3'] = p3
        else:
            p3 = figure(title="No Data for Profits")
            plots['chart3'] = p3

        # =========== 4 =============

        df4 = get_classroom_availability()


        if not df4.empty:
            df4['room_number'] = df4['room_number'].astype(str)
            source4 = ColumnDataSource(df4)
            rooms = df4["room_number"].to_list()
            p4 = figure(y_range=rooms, height=350, title="Classroom Availability",
                        toolbar_location=None, tools="")
            p4.hbar(y='room_number', right='lessons_count', height=0.8, source=source4,
                    line_color='white', fill_color="#2b948f")
            p4.add_tools(HoverTool(tooltips=[("Room", "@room_number"), ("Lessons", "@lessons_count")]))
            plots['chart4'] = p4
        else:
            p4 = figure(title="No Data for Classrooms")
            plots['chart4'] = p4


        # =========== 5 =============
        df5 = get_payments_by_method()


        if not df5.empty:
            df5['total'] = df5['total'].astype(float)
            df5['angle'] = df5['total'] / df5['total'].sum() * 2 * pi
            df5['color'] = [Turbo256[i*20%256] for i in range(len(df5))]
            
            source5 = ColumnDataSource(df5)

            p5 = figure(height=350, title="Payment Methods", toolbar_location=None,
                        tools="hover", tooltips="@method: @total", x_range=(-0.5, 1.0))
            
            p5.wedge(x=0, y=1, radius=0.4,
                             start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                             line_color="white", fill_color='color', legend_field='method', source=source5)
            
            p5.axis.visible = False
            p5.grid.grid_line_color = None
            plots['chart5'] = p5
        else:
            p5 = figure(title="No Data for Payments")
            plots['chart5'] = p5


        # =========== 6 =============
    
        df_income = get_monthly_income()

        if not df_income.empty:
            df_income['monthly_income'] = df_income['monthly_income'].astype(float)
            source6 = ColumnDataSource(df_income)

            p6 = figure(height=400, title="Monthly profit", x_axis_label='Month', y_axis_label='Income',
                       toolbar_location=None, tools="hover", tooltips=[("Month", "@month"), ("monthly_income", "@monthly_income")])

            p6.line(x='month', y='monthly_income', source=source6, line_width=3, line_color="green")
            p6.circle(x='month', y='monthly_income', source=source6, fill_color="white", size=8, line_color="green")
            
            plots['chart6'] = p6
        else:
            p6 = figure(title="No Data for Monthly Income")
            plots['chart6'] = p6

        script, divs = components(plots)

        js_resourses = CDN.render()
        context = {
            'script': script,
            'divs':divs,
            'min_courses': min_courses,
            'min_grade': min_grade,
            'resources': js_resourses
        }
         
        return render(request, 'itcourses_ui/dashboard_bokeh.html', context)
       


class ParallelBenchmarkDashboard(View):
    def get(self, request):
        data = benchmark()
        df = pd.DataFrame(data)

        fig = px.line(
            df,
            x="threads",
            y="time_sec",
            markers=True,
            title="Execution time vs number of threads",
            labels={
                "threads": "Number of threads",
                "time_sec": "Execution time (sec)"
            }
        )

        chart = pio.to_html(fig, full_html=False)

        return render(
            request,
            "itcourses_ui/dashboard_benchmark.html",
            {"chart": chart}
        )
