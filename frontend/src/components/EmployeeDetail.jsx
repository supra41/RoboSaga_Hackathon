import { useParams } from 'react-router-dom';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer, Legend } from 'recharts';
import Navbar from './Navbar';
import axios from 'axios';

const employees = [
  { id: 1, name: 'Rohan Sharma', role: 'Software Engineer', status: 'Active' },
  { id: 2, name: 'Ananya Verma', role: 'UI/UX Designer', status: 'Away' },
  { id: 3, name: 'Karan Mehta', role: 'Data Analyst', status: 'Distracted' },
];

const productivityData = [
  { date: 'Mon', focusTime: 5, distractions: 2 },
  { date: 'Tue', focusTime: 6, distractions: 1 },
  { date: 'Wed', focusTime: 4, distractions: 3 },
  { date: 'Thu', focusTime: 7, distractions: 1 },
  { date: 'Fri', focusTime: 6, distractions: 2 },
];

const dailyBreakdownData = [
  { day: 'Mon', activeWork: 5, idleTime: 2, breaks: 1 },
  { day: 'Tue', activeWork: 6, idleTime: 1, breaks: 2 },
  { day: 'Wed', activeWork: 4, idleTime: 3, breaks: 1 },
  { day: 'Thu', activeWork: 7, idleTime: 1, breaks: 1 },
  { day: 'Fri', activeWork: 6, idleTime: 2, breaks: 2 },
];

const attendanceData = [
  { name: 'Online Hours', value: 40 },
  { name: 'Offline Hours', value: 20 },
];

const COLORS = ['#4CAF50', '#F44336'];

// const [data, setData] = useState(null);

//   useEffect(() => {
//     const fetchData = async () => {
//       try {
//         const response = await axios.post('https://your-api-endpoint.com/employee-data', { employeeId: id });
//         setData(response.data);
//       } catch (error) {
//         console.error("Error fetching data:", error);
//       }
//     };
//     fetchData();
//   }, [id]);

export default function EmployeeDetail() {
  const { id } = useParams();
  const employee = employees.find(emp => emp.id === parseInt(id));

  if (!employee) {
    return <div className="text-center text-red-500 mt-10">Employee not found</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="w-full max-w-6xl mx-auto bg-white shadow-lg rounded-lg p-6 mt-6">
        
        {/* Employee Details */}
        <div className="flex items-center space-x-6 p-6 bg-gray-100 rounded-lg">
          <div className="w-24 h-24 bg-blue-500 text-white flex items-center justify-center rounded-full text-3xl font-semibold">
            {employee.name.charAt(0)}
          </div>
          <div className="flex-1">
            <h2 className="text-3xl font-semibold text-gray-800">{employee.name}</h2>
            <p className="text-lg text-gray-500">{employee.role}</p>
            <p className={`text-sm mt-2 font-medium ${
              employee.status === 'Active' ? 'text-green-500' : 
              employee.status === 'Away' ? 'text-yellow-500' : 'text-red-500'
            }`}>
              Status: {employee.status}
            </p>
          </div>
        </div>

        {/* Real-Time Monitoring */}
        <div className="w-full bg-gray-100 p-4 rounded-lg my-6">
          <h3 className="text-lg font-medium text-gray-700 mb-2">Real-Time Monitoring</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-gray-700">
            <p><strong>Live Status:</strong> {employee.status}</p>
            <p><strong>AFK Timer:</strong> 10 min</p>
            <p><strong>Current App Focus:</strong> VS Code</p>
            <p><strong>Daily Productivity Score:</strong> 85%</p>
          </div>
        </div>

        {/* Graphs Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          
          {/* Productivity Chart */}
          <div className="bg-gray-100 p-4 rounded-lg">
            <h3 className="text-lg font-medium text-gray-700 mb-4">Productivity Analysis</h3>
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={productivityData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="focusTime" stroke="#4CAF50" name="Focus Time (hrs)" />
                <Line type="monotone" dataKey="distractions" stroke="#F44336" name="Distractions" />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Daily Productivity Breakdown */}
          <div className="bg-gray-100 p-4 rounded-lg">
            <h3 className="text-lg font-medium text-gray-700 mb-4">Daily Productivity Breakdown</h3>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={dailyBreakdownData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="activeWork" fill="#4CAF50" name="Active Work (hrs)" />
                <Bar dataKey="idleTime" fill="#FF9800" name="Idle Time (hrs)" />
                <Bar dataKey="breaks" fill="#F44336" name="Breaks (hrs)" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Attendance & Active Hours */}
          <div className="col-span-1 lg:col-span-2 bg-gray-100 p-4 rounded-lg">
            <h3 className="text-lg font-medium text-gray-700 mb-4">Attendance & Active Hours</h3>
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Tooltip />
                <Legend />
                <Pie data={attendanceData} dataKey="value" nameKey="name" outerRadius={100} label>
                  {attendanceData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
          </div>

        </div>
      </div>
    </div>
  );
}


