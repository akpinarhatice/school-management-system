from django.shortcuts import render, redirect, HttpResponseRedirect
from people.models import Member #models.py
from people.models import School #models.py
from people.models import Class #models.py
from people.models import Student #models.py
from people.models import Teacher #models.py
from people.models import Manager #models.py
from django.shortcuts import get_object_or_404, render
# Create your views here.
def index(request):
    return render(request, 'index.html')
def addSchool(request):
    if request.method == 'POST':
        school1 = School(name=request.POST['name1'], city=request.POST['city1'])
        school1.save()
        school2 = School(name=request.POST['name2'], city=request.POST['city2'])
        school2.save()
        school3 = School(name=request.POST['name3'], city=request.POST['city3'])
        school3.save()
        schools = School.objects.all().order_by("name")
        names=["A","B","C","D"]
        for school in schools:
            sinif1 = Class(name=names[0], okul_id=school.id)
            sinif2 = Class(name=names[1], okul_id=school.id)
            sinif3 = Class(name=names[2], okul_id=school.id)
            sinif4 = Class(name=names[3], okul_id=school.id)
            sinif1.save()
            sinif2.save()
            sinif3.save()
            sinif4.save()
        return redirect('/register')
    else:
        return render(request, 'addSchool.html')

def register(request):
    schools = School.objects.all()
    classes = Class.objects.all()
    if request.method == 'POST':
        if request.POST['type']=="student":
            member = Student(firstname=request.POST['firstname'], lastname=request.POST['lastname'],  email=request.POST['email'],  password=request.POST['password'], class_id=request.POST['class'])
            member.save()
            return redirect('/login')
        if request.POST['type']=="teacher":
            member = Teacher(firstname=request.POST['firstname'], lastname=request.POST['lastname'],  email=request.POST['email'],  password=request.POST['password'], class_id=request.POST['class'])
            member.save()
            return redirect('/login')
        if request.POST['type']=="manager":
            member = Manager(firstname=request.POST['firstname'], lastname=request.POST['lastname'],  email=request.POST['email'],  password=request.POST['password'], okul_id=request.POST['school'])
            member.save()
            return redirect('/login')
    else:
        return render(request, 'register.html',{"schools":schools,"classes":classes})

def login(request):
    if request.method == 'POST':

        email = request.POST['email']
        password = request.POST['password']
        students = Student.objects.all()
        teachers = Teacher.objects.all()
        managers = Manager.objects.all()
        for student in students:
            if student.email==email and student.password==password:
                print(student.email)
                class_id=student.class_id
                classes = Class.objects.all()
                for classTmp in classes:
                    if classTmp.id==class_id:
                        classObject=classTmp

                teachers = Teacher.objects.all()
                selectedTeacher="Atanmadı"
                for teacher in teachers:
                    if teacher.class_id==class_id:
                        selectedTeacher=teacher
                return render(request,'student.html',{"email":student.email,"firstname":student.firstname,"lastname":student.lastname,"password":student.password,"classObject":classObject,"selectedTeacher":selectedTeacher})
        for teacher in teachers:
            if teacher.email==email and teacher.password==password:
                class_id=teacher.class_id
                classes = Class.objects.all()
                for classTmp in classes:
                    if classTmp.id==class_id:
                        classObject=classTmp
                students = Student.objects.all()
                studentObjects=[]
                for student in students:
                    if student.class_id==class_id:
                        print(student.firstname)
                        studentObjects.append(student)
                classes = Class.objects.all()
                classObjects=[]
                for clas in classes:
                    if clas.id==class_id:
                        classObjects.append(clas)
                return render(request,'teacher.html',{"teacher":teacher,"classObject":classObject,"studentObjects":studentObjects,"classObjects":classObjects})
        for manager in managers:
            if manager.email==email and manager.password==password:
                okul_id = manager.okul_id
                school = School.objects.get(id=okul_id)
                classes = Class.objects.all()
                classObjects=[]
                for clas in classes:
                    if clas.okul_id==okul_id:
                        classObjects.append(clas)
                teachers = Teacher.objects.all()
                for i in range(len(classObjects)):
                    print(classObjects[i].id)
                teacherObjects=[]
                for teacher in teachers:
                    for clas in classObjects:
                        print(clas.id,teacher.class_id)
                        if clas.id==teacher.class_id:
                            teacherObjects.append(teacher)
                            break

                return render(request,'manager.html',{"manager":manager,"teacherObjects":teacherObjects})
        return redirect('/login')


    else:
        return render(request, 'login.html')
def student(request):
    return render(request, 'student.html')
def update(request,id):
    student=Student.objects.get(id=id)
    classes = Class.objects.all()

    for classTmp in classes:
        if classTmp.id==student.class_id:
            classObject=classTmp;
            break
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        Student.objects.filter(id=student.id).update(firstname=firstname,lastname=lastname,email=email)
        teachers = Teacher.objects.all()
        for teacher in teachers:
            if teacher.class_id==student.class_id:
                selectedTeacher=teacher
        class_id = selectedTeacher.class_id
        classes = Class.objects.all()
        for classTmp in classes:
            if classTmp.id == class_id:
                classObject = classTmp
        students = Student.objects.all()
        studentObjects = []
        for student in students:
            if student.class_id == class_id:
                print(student.firstname)
                studentObjects.append(student)
        return render(request,'teacher.html',{"teacher":selectedTeacher,"classObject":classObject,"studentObjects":studentObjects})

    else:
        return render(request, 'update.html', {'student': student,'classes': classes,'classObject': classObject})
def delete(request,id):
    student=Student.objects.get(id=id)
    Student.objects.filter(id=id).delete()
    teachers = Teacher.objects.all()
    for teacher in teachers:
        if teacher.class_id == student.class_id:
            selectedTeacher = teacher
    class_id = selectedTeacher.class_id
    classes = Class.objects.all()
    for classTmp in classes:
        if classTmp.id == class_id:
            classObject = classTmp
    students = Student.objects.all()
    studentObjects = []
    for student in students:
        if student.class_id == class_id:
            print(student.firstname)
            studentObjects.append(student)
    return render(request,'teacher.html',{"teacher":selectedTeacher,"classObject":classObject,"studentObjects":studentObjects})

def manager(request):
    teachers = Teacher.objects.all().order_by("firstname")
    return render(request, 'manager.html', {"teacher": teachers})
def teacher(request):
    return render(request, 'teacher.html')
