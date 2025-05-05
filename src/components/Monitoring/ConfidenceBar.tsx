
import React from "react";
import { cn } from "@/lib/utils";
import { Progress } from "@/components/ui/progress";
import { DetectionType } from "./DetectionItem";

interface ConfidenceBarProps {
  confidence: number;
  type: DetectionType;
}

const ConfidenceBar: React.FC<ConfidenceBarProps> = ({ confidence, type }) => {
  const percentage = Math.round(confidence * 100);
  
  const getColor = () => {
    if (type === 'financial') {
      return percentage > 85 ? "bg-ts-pink-500" : 
             percentage > 50 ? "bg-ts-pink-400" : "bg-ts-pink-300";
    }
    
    return percentage > 85 ? "bg-ts-purple-500" : 
           percentage > 50 ? "bg-ts-purple-400" : "bg-ts-purple-300";
  };
  
  return (
    <div className="flex items-center gap-2">
      <span className="text-xs whitespace-nowrap">{percentage}% confidence</span>
      <Progress 
        value={percentage} 
        className="h-2 w-24"
        indicatorClassName={cn(getColor())}
      />
    </div>
  );
};

export default ConfidenceBar;
