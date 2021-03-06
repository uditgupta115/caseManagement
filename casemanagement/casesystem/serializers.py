from rest_framework import serializers
from casemanagement.casesystem.models import Task, Case, User, UserRole


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'role', 'task_name', 'task_status', 'remarks')


class CaseSerializer(serializers.ModelSerializer):
    task = TaskSerializer(required=False, many=True)

    class Meta:
        model = Case
        fields = ('id', 'task', 'role', 'case_name', 'case_status', 'remarks')

    def create(self, validated_data):
        task_data = validated_data.pop('task', {})
        case = Case.objects.create(**validated_data)
        if task_data:
            for count, _ in enumerate(task_data):
                task, _ = Task.objects.update_or_create(case=case, **task_data[count])
        return case

    def update(self, case, validated_data):
        task_data = validated_data.pop('task', {})
        if task_data:
            task_set = case.task_set.all()
            for count, task in enumerate(task_data):
                task_set[count].__dict__.update(task_data[count])
                task_set[count].save()
        case.__dict__.update(**validated_data)
        case.save()
        return case


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ('id', 'role')


class UserSerializer(serializers.ModelSerializer):
    userrole = UserRoleSerializer(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'email', 'password', 'last_name', 'userrole')

    def create(self, validated_data):
        userrole = validated_data.pop('userrole', {})
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        UserRole.objects.create(user=user, role=userrole.get('role', 0))
        user.save()
        return user

    def update(self, user, validated_data):
        userrole = validated_data.pop('userrole', {})
        if userrole:
            user_role = user.userrole
            user_role.__dict__.update(**userrole)
            user_role.save()
        user.__dict__.update(**validated_data)
        user.save()
        return user
