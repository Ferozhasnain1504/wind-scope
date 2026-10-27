import {
  Activity,
  ChartNoAxesCombined,
  LayoutDashboard,
  Wind,
} from "lucide-react";

const navigation = [
  { label: "Overview", icon: LayoutDashboard },
  { label: "Forecast accuracy", icon: ChartNoAxesCombined },
  { label: "Forecast explorer", icon: Activity },
];

export default function AppSidebar({ activePage, onNavigate }) {
  return (
    <aside className="flex min-h-screen w-64 shrink-0 flex-col border-r border-stone-200 bg-white px-5 py-6">
      <div className="flex items-center gap-3 px-2">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-800 text-white">
          <Wind size={22} />
        </div>

        <div>
          <h1 className="text-lg font-semibold tracking-tight text-stone-900">
            WindScope
          </h1>
          <p className="text-xs text-stone-500">Energy intelligence</p>
        </div>
      </div>

      <div className="mt-10">
        <p className="mb-3 px-3 text-[11px] font-semibold uppercase tracking-[0.16em] text-stone-400">
          Workspace
        </p>

        <nav className="space-y-1">
          {navigation.map(({ label, icon: Icon }) => {
            const active = activePage === label;

            return (
              <button
                key={label}
                onClick={() => onNavigate(label)}
                className={`flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-left text-sm transition-colors ${
                  active
                    ? "bg-emerald-50 font-medium text-emerald-900"
                    : "text-stone-600 hover:bg-stone-50 hover:text-stone-900"
                }`}
              >
                <Icon size={18} strokeWidth={1.8} />
                {label}
              </button>
            );
          })}
        </nav>
      </div>

      <div className="mt-auto rounded-xl border border-stone-200 bg-stone-50 p-4">
        <div className="flex items-center gap-2 text-sm font-medium text-stone-800">
          <span className="h-2 w-2 rounded-full bg-emerald-600" />
          Data workspace
        </div>
        <p className="mt-2 text-xs leading-5 text-stone-500">
          UK wind generation
          <br />
          30-minute resolution
        </p>
      </div>
    </aside>
  );
}