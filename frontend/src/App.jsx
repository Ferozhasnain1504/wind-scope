import { useEffect, useState } from "react";
import { getOverview, getAccuracy } from "@/services/api";
import {
  ArrowDownRight,
  ArrowUpRight,
  CalendarDays,
  Download,
  Wind,
  Zap,
  Target,
  Activity,
} from "lucide-react";

import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";

import AppSidebar from "@/components/app-sidebar";
import MetricCard from "@/components/metric-card";
import GenerationChart from "@/components/generation-chart";

function formatMW(value) {
  if (value === null || value === undefined || !Number.isFinite(Number(value))) {
    return "—";
  }

  return Number(value).toLocaleString("en-GB", {
    maximumFractionDigits: 1,
  });
}

export default function App() {
  const [activePage, setActivePage] = useState("Overview");
  const [selectedDate, setSelectedDate] = useState("2026-01-01");
  const [overview, setOverview] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [monthlyAccuracy, setMonthlyAccuracy] = useState(null);
  const [accuracyLoading, setAccuracyLoading] = useState(true);
  const [accuracyError, setAccuracyError] = useState("");

  useEffect(() => {
    let cancelled = false;

    async function loadOverview() {
      setLoading(true);
      setError("");

      try {
        const result = await getOverview(selectedDate);

        if (!cancelled) {
          setOverview(result);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err.message || "Unable to load wind generation data.");
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadOverview();

    return () => {
      cancelled = true;
    };
  }, [selectedDate]);


  useEffect(() => {
    let cancelled = false;

    async function loadMonthlyAccuracy() {
      setAccuracyLoading(true);
      setAccuracyError("");

      try {
        const result = await getAccuracy("2026-01-01", "2026-01-31");

        if (!cancelled) {
          setMonthlyAccuracy(result);
        }
      } catch (err) {
        if (!cancelled) {
          setAccuracyError(
            err.message || "Unable to load monthly accuracy."
          );
        }
      } finally {
        if (!cancelled) {
          setAccuracyLoading(false);
        }
      }
    }

    loadMonthlyAccuracy();

    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <div className="min-h-screen bg-[#f7f8f5] text-stone-900">
      <div className="flex min-h-screen">
        <AppSidebar
          activePage={activePage}
          onNavigate={setActivePage}
        />

        <main className="min-w-0 flex-1">
          <header className="flex flex-wrap items-center justify-between gap-4 border-b border-stone-200 bg-white px-6 py-4 lg:px-9">
            <div>
              <p className="text-xs text-stone-500">
                Energy markets / Wind generation
              </p>
              <h2 className="mt-1 text-lg font-semibold tracking-tight">
                {activePage}
              </h2>
            </div>

            <div className="flex items-center gap-3">
              <Badge
                variant="outline"
                className="border-amber-200 bg-amber-50 text-amber-800"
              >
                Sample data
              </Badge>

              <Button
                variant="outline"
                className="border-stone-200 bg-white"
                onClick={() => window.print()}
              >
                <Download size={16} />
                <span className="ml-2">Export view</span>
              </Button>
            </div>
          </header>

          <div className="mx-auto max-w-[1500px] space-y-7 px-5 py-7 lg:px-9 lg:py-9">
            <section className="flex flex-wrap items-end justify-between gap-4">
              <div>
                <p className="text-sm font-medium text-emerald-800">
                  UK NATIONAL GENERATION
                </p>

                <h1 className="mt-2 text-3xl font-semibold tracking-tight">
                  Wind generation overview
                </h1>

                <p className="mt-2 max-w-2xl text-sm leading-6 text-stone-500">
                  Understand forecast availability, generation outcomes
                  and forecast accuracy for day-ahead decisions.
                </p>
              </div>

              <Button
                variant="outline"
                className="border-stone-200 bg-white"
              >
                <CalendarDays size={16} />
                <span className="ml-2">January 2026</span>
              </Button>
            </section>

            {error && (
          <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-800">
            {error}
          </div>
        )}

        {loading && (
          <p className="text-sm text-stone-500">
            Loading generation data…
          </p>
        )}

        {!loading && !error && overview && (
          <div className="rounded-lg border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-900">
            Data loaded from the WindScope API for {overview.delivery_date}.
            Forecast cutoff assumption: {overview.forecast_cutoff}.
          </div>
        )}

            <section className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
              {accuracyError && (
                <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-800">
                  Monthly accuracy unavailable: {accuracyError}
                </div>
              )}
              <MetricCard
                title="Forecast generation"
                value={loading ? "…" : formatMW(overview?.data?.[0]?.forecast)}
                unit="MW"
                description="First available hourly interval"
                icon={Wind}
              />

              <MetricCard
                title="Actual generation"
                value={loading ? "…" : formatMW(overview?.data?.[0]?.actual)}
                unit="MW"
                description="Illustrative observed generation"
                icon={Zap}
              />

              
              <MetricCard
                title="January MAE"
                value={
                  accuracyLoading
                    ? "…"
                    : formatMW(monthlyAccuracy?.metrics?.mae)
                }
                unit="MW"
                description="Average absolute error · Jan 2026"
                icon={Target}
              />


              
              <MetricCard
                title="January forecast bias"
                value={
                  accuracyLoading
                    ? "…"
                    : formatMW(monthlyAccuracy?.metrics?.bias)
                }
                unit="MW"
                description="Positive means forecasts exceed actuals"
                icon={Activity}
              />

            </section>

            <section>
              <Card className="rounded-xl border-stone-200 bg-white shadow-none">
                <CardContent className="p-5 lg:p-7">
                  <div className="flex flex-wrap items-start justify-between gap-3">
                    <div>
                      <h3 className="font-semibold tracking-tight">
                        Forecast vs actual generation
                      </h3>

                      <p className="mt-1 text-sm text-stone-500">
                        Illustrative generation profile · MW
                      </p>
                    </div>

                    <Badge variant="outline" className="font-normal">
                      30-minute data
                    </Badge>
                  </div>

                  <Separator className="my-5 bg-stone-100" />

                  <GenerationChart data={overview?.data ?? []} />
                </CardContent>
              </Card>
            </section>

            <section className="grid grid-cols-1 gap-4 xl:grid-cols-2">
              <Card className="rounded-xl border-stone-200 bg-white shadow-none">
                <CardContent className="p-5">
                  <h3 className="font-semibold">
                    Forecast interpretation
                  </h3>

                  <p className="mt-2 text-sm leading-6 text-stone-500">
                    Forecast errors help traders understand uncertainty
                    in expected wind output. Underforecasting and
                    overforecasting can have different operational
                    implications.
                  </p>

                  <div className="mt-5 flex items-start gap-3 rounded-lg bg-stone-50 p-4">
                    <ArrowUpRight
                      size={19}
                      className="mt-0.5 text-emerald-700"
                    />

                    <div>
                      <p className="text-sm font-medium">
                        Positive forecast bias
                      </p>

                      <p className="mt-1 text-xs leading-5 text-stone-500">
                        Forecast generation exceeds actual generation
                        on average over the selected sample.
                      </p>
                    </div>
                  </div>

                  <div className="mt-3 flex items-start gap-3 rounded-lg bg-stone-50 p-4">
                    <ArrowDownRight
                      size={19}
                      className="mt-0.5 text-amber-700"
                    />

                    <div>
                      <p className="text-sm font-medium">
                        Negative forecast bias
                      </p>

                      <p className="mt-1 text-xs leading-5 text-stone-500">
                        Forecast generation falls below actual
                        generation on average over the selected sample.
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="rounded-xl border-stone-200 bg-white shadow-none">
                <CardContent className="p-5">
                  <h3 className="font-semibold">
                    Data coverage
                  </h3>

                  <p className="mt-1 text-sm text-stone-500">
                    Intended scope for the pilot
                  </p>

                  <Separator className="my-4 bg-stone-100" />

                  <div className="space-y-4 text-sm">
                    <div className="flex justify-between gap-3">
                      <span className="text-stone-500">Geography</span>
                      <span className="font-medium">UK national</span>
                    </div>

                    <div className="flex justify-between gap-3">
                      <span className="text-stone-500">Generation type</span>
                      <span className="font-medium">Wind</span>
                    </div>

                    <div className="flex justify-between gap-3">
                      <span className="text-stone-500">Resolution</span>
                      <span className="font-medium">30 minutes</span>
                    </div>

                    <div className="flex justify-between gap-3">
                      <span className="text-stone-500">Analysis window</span>
                      <span className="font-medium">January 2026</span>
                    </div>

                    <div className="flex justify-between gap-3">
                      <span className="text-stone-500">Data source</span>
                      <span className="font-medium">Elexon (planned)</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </section>

            <footer className="border-t border-stone-200 pt-5 text-xs leading-5 text-stone-500">
              WindScope · Day-ahead wind forecast analytics ·
              Sample data until the Elexon integration is complete.
            </footer>
          </div>
        </main>
      </div>
    </div>
  );
}
