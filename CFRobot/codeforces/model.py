class UserSubmission:

    def __init__(self, name, handle, ac_number, total, problem_list):
        self.name = name
        self.handle = handle
        self.ac_number = ac_number
        self.total = total
        self.problem_list = problem_list

    def __lt__(self, other):
        if self.ac_number == other.ac_number:
            return self.total < other.total
        return self.ac_number < other.ac_number

    def to_String(self):
        message = "name      :  " + self.name + "\n" \
                + "handle    :  " + self.handle + "\n" \
                + "刷题总数 :  " + str(self.ac_number) + "\n"\
                + "总提交数 :  " + str(self.total) + "\n" \
                + "过题列表 :  "
        if len(self.problem_list) == 0:
            message += "[空空如也!!!]\n\n"
            return message
        message += "\n[\n"
        for i in self.problem_list:
            message += " 	题目编号 : " + str(i["pname"]) + "\n" \
                     + " 	题目分值 : " + str(i["pscore"]) + "\n" \
                     + " 	过题时间 : " + i["pass_time"] + "\n\n"
        message += "]\n"
        return message


