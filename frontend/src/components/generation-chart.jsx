import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

export default function GenerationChart({ data = [] }) {
  const chartData = data.map((item) => ({
    time: item.startTime
      ? new Date(item.startTime).toLocaleTimeString("en-GB", {
          hour: "2-digit",
          minute: "2-digit",
          timeZone: "UTC",
        })
      : "",
    forecast:
      item.forecast === null || item.forecast === undefined
        ? null
        : Number(item.forecast),
    actual:
      item.actual === null || item.actual === undefined
        ? null
        : Number(item.actual),
  }));

  return (
    <div className="h-[320px] w-full">
      {chartData.length === 0 ? (
        <div className="flex h-full items-center justify-center text-sm text-stone-500">
          No generation data available for this date.
        </div>
      ) : (
        <ResponsiveContainer width="100%" height="100%">
          <LineChart
            data={chartData}
            margin={{ top: 12, right: 12, left: 0, bottom: 4 }}
          >
            <CartesianGrid
              stroke="#e7e5e4"
              strokeDasharray="3 3"
              vertical={false}
            />

            <XAxis
              dataKey="time"
              tick={{ fill: "#78716c", fontSize: 12 }}
              tickLine={false}
              axisLine={false}
              tickMargin={12}
            />

            <YAxis
              tick={{ fill: "#78716c", fontSize: 12 }}
              tickLine={false}
              axisLine={false}
              width={58}
              tickFormatter={(value) => `${value / 1000}k`}
            />

            <Tooltip
              contentStyle={{
                borderRadius: 10,
                border: "1px solid #e7e5e4",
                fontSize: 12,
              }}
              formatter={(value, name) => [
                value == null
                  ? "No data"
                  : `${Number(value).toLocaleString("en-GB")} MW`,
                name === "forecast" ? "Forecast" : "Actual",
              ]}
              labelFormatter={(label) => `Time: ${label} UTC`}
            />

            <Legend
              verticalAlign="top"
              align="right"
              height={36}
              iconType="circle"
              iconSize={8}
            />

            <Line
              type="monotone"
              dataKey="forecast"
              name="Forecast"
              stroke="#047857"
              strokeWidth={2.5}
              dot={false}
              activeDot={{ r: 4 }}
              connectNulls={false}
            />

            <Line
              type="monotone"
              dataKey="actual"
              name="Actual"
              stroke="#D97706"
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 4 }}
              connectNulls={false}
            />
          </LineChart>
        </ResponsiveContainer>
      )}
    </div>
  );
}