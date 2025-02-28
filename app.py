import { useState } from "react";
import { Slider } from "@/components/ui/slider";
import { Card, CardContent } from "@/components/ui/card";
import { motion } from "framer-motion";
import { Radar } from "recharts";

export default function EcoShopAI() {
  const [scores, setScores] = useState({
    material: 5,
    carbon: 5,
    packaging: 5,
  });

  const totalScore = ((scores.material + scores.carbon + scores.packaging) / 3).toFixed(1);
  const ecoRating = totalScore > 7 ? "Eco-Friendly" : totalScore > 4 ? "Moderate" : "Not Eco-Friendly";
  const radarData = [
    { subject: "Material", value: scores.material },
    { subject: "Carbon Footprint", value: scores.carbon },
    { subject: "Packaging", value: scores.packaging },
  ];

  return (
    <div className="min-h-screen bg-gray-900 text-white p-10 flex flex-col items-center">
      <motion.h1 className="text-4xl font-bold mb-6" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>EcoShop AI - Sustainable Shopping Assistant</motion.h1>
      <p className="mb-4 text-gray-400">Enter product details to check its eco-friendliness.</p>
      
      <Card className="p-6 w-full max-w-lg bg-gray-800 rounded-2xl shadow-lg">
        <CardContent>
          {Object.keys(scores).map((key) => (
            <div key={key} className="mb-5">
              <p className="text-sm mb-1 capitalize">{key} Score (1-10)</p>
              <Slider value={[scores[key]]} min={1} max={10} step={1} onValueChange={(val) => setScores({ ...scores, [key]: val[0] })} className="text-red-500" />
            </div>
          ))}
        </CardContent>
      </Card>
      
      <motion.div className="mt-6 p-4 bg-gray-800 rounded-xl shadow-md text-center" initial={{ scale: 0.9 }} animate={{ scale: 1 }}>
        <h2 className="text-lg font-semibold">Eco Score: {totalScore}/10</h2>
        <p className={`text-lg font-bold mt-1 ${ecoRating === "Eco-Friendly" ? "text-green-400" : ecoRating === "Moderate" ? "text-yellow-400" : "text-red-400"}`}>{ecoRating}</p>
      </motion.div>
      
      <div className="mt-6 w-full max-w-md">
        <Radar width={400} height={300} data={radarData} />
      </div>
    </div>
  );
}
