import { Card, CardContent } from "@/components/ui/card";

export default function MetricCard({
  title,
  value,
  unit,
  description,
  icon: Icon,
}) {
  return (
    <Card className="rounded-xl border-stone-200 bg-white shadow-none">
      <CardContent className="p-5">
        <div className="flex items-start justify-between gap-3">
          <div>
            <p className="text-sm text-stone-500">{title}</p>
            <div className="mt-3 flex items-baseline gap-1.5">
              <span className="text-2xl font-semibold tracking-tight text-stone-900">
                {value}
              </span>
              {unit && (
                <span className="text-sm text-stone-500">{unit}</span>
              )}
            </div>
          </div>

          {Icon && (
            <div className="rounded-lg border border-stone-200 p-2 text-stone-500">
              <Icon size={18} strokeWidth={1.7} />
            </div>
          )}
        </div>

        <p className="mt-3 text-xs leading-5 text-stone-500">
          {description}
        </p>
      </CardContent>
    </Card>
  );
}