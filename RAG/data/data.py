productDetails = [
    {
        "page_content": "PeopleHub's employee tracking feature allows managers to monitor work hours, employee availability, and productivity. You can set up real-time alerts if employees deviate from expected productivity levels or schedules. The system also generates daily, weekly, and monthly reports to track attendance and individual performance trends.",
        "metadata": {"feature": "Employee Tracking", "category": "Core Feature"}
    },
    {
        "page_content": "PeopleHub's performance review feature provides a structured approach to employee evaluations. Managers can set custom evaluation criteria for each role, rate employees on multiple metrics, and add comments. Performance reviews are automatically integrated into individual development plans, allowing both managers and employees to track growth over time.",
        "metadata": {"feature": "Performance Reviews", "category": "Core Feature"}
    },
    {
        "page_content": "The goal-setting module in PeopleHub allows both team leads and individual employees to set clear, measurable goals. Progress tracking is available on a visual dashboard, with notifications sent as deadlines approach. Managers can set team-wide targets as well as personal objectives for employees, keeping everyone aligned with organizational goals.",
        "metadata": {"feature": "Goal Setting", "category": "Core Feature"}
    },
    {
        "page_content": "With PeopleHub's productivity insights, managers can analyze patterns in employee efficiency, such as task completion times and overall productivity trends. These insights are powered by AI to help identify top performers and provide a basis for workload balancing and performance improvement.",
        "metadata": {"feature": "Productivity Insights", "category": "Core Feature"}
    },
    {
        "page_content": "PeopleHub's project alignment feature enables managers to assign resources to tasks based on project timelines and team capacity. With a real-time project dashboard, managers can view task dependencies, track resource allocation, and adjust project plans as needed. This helps ensure that team efforts align with project milestones and organizational priorities.",
        "metadata": {"feature": "Project Alignment", "category": "Project Management"}
    },
    {
        "page_content": "The employee wellbeing feature in PeopleHub helps monitor engagement and satisfaction. Through anonymous surveys, employees can share feedback on stress levels and overall morale, allowing managers to gain insights into team wellbeing. Privacy is prioritized, and managers receive only aggregated data and trends, helping them improve morale without compromising confidentiality.",
        "metadata": {"feature": "Employee Wellbeing", "category": "Wellbeing and Engagement"}
    },
    {
        "page_content": "PeopleHub offers integrations with popular tools such as Slack, Zoom, Asana, and ADP. This enables seamless data flow across platforms, making it easy for HR and team leads to track productivity and manage payroll within the tools they already use. This integration helps create a unified employee management system.",
        "metadata": {"feature": "Integration Capabilities", "category": "Integrations"}
    }
]


allPrompts = [
    {
        "page_content": "The user asked about tracking employee {metric} in PeopleHub. Include details on how the tracking works, key features, and any options for customization.",
        "metadata": {"context": "Employee Tracking Query", "example": "How does PeopleHub help track employee hours?"}
    },
    {
        "page_content": "The user is inquiring about the performance review process. Explain PeopleHub's structured review approach, customization options, and how reviews feed into employee growth plans.",
        "metadata": {"context": "Performance Review Query", "example": "How can I do performance reviews in PeopleHub?"}
    },
    {
        "page_content": "The user asked about productivity insights and goal setting for a team in PeopleHub. Include available metrics, tracking capabilities, and examples of insights generated.",
        "metadata": {"context": "Productivity and Goal Setting Query", "example": "Can PeopleHub track team productivity?"}
    },
    {
        "page_content": "The user is interested in PeopleHub's wellbeing monitoring feature. Explain how wellbeing data is collected, privacy considerations, and actionable insights for managers.",
        "metadata": {"context": "Employee Wellbeing Query", "example": "How does PeopleHub monitor employee wellbeing?"}
    },
    {
        "page_content": "The user has expressed that they do not want to set up a meeting. Provide alternative options for getting help or addressing their query within PeopleHub’s features.",
        "metadata": {"context": "Reluctance to Schedule Meeting", "example": "I don't really want to schedule a meeting right now; is there another way to get help?"}
    }
]
