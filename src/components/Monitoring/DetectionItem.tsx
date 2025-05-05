import React from "react";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import ConfidenceBar from "./ConfidenceBar";

export type DetectionType = 'personal' | 'financial';

export interface Detection {
  id: string;
  timestamp: Date;
  value: string;
  type: DetectionType;
  source: string;
  confidence: number;
}

interface DetectionItemProps {
  detection: Detection;
  onEncrypt?: (id: string) => void;
  onIgnore?: (id: string) => void;
}

const DetectionItem: React.FC<DetectionItemProps> = ({
  detection,
  onEncrypt,
  onIgnore,
}) => {
  const { id, timestamp, value, type, source, confidence } = detection;

  const typeColors: Record<DetectionType, string> = {
    personal: 'bg-ts-purple-100 text-ts-purple-800 border-ts-purple-200',
    financial: 'bg-ts-pink-100 text-ts-pink-800 border-ts-pink-200'
  };

  const formattedDate = new Intl.DateTimeFormat('en-US', {
    dateStyle: 'medium',
    timeStyle: 'short'
  }).format(timestamp);

  // Mask the value based on its type
  const maskValue = (val: string, type: DetectionType): string => {
    if (type === 'personal') {
      return val.replace(/\w/g, '*');
    }
    // For financial data, keep first and last characters
    if (type === 'financial' && val.length > 4) {
      return val.slice(0, 2) + '*'.repeat(val.length - 4) + val.slice(-2);
    }
    return '*'.repeat(val.length);
  };

  return (
    <Card className={cn(
      "relative overflow-hidden transition-all duration-300 hover:shadow-md",
      confidence > 0.85 ? "border-l-4 pulse-border" : "",
      confidence > 0.85 && type === 'financial' ? "border-l-ts-pink-500" : "",
      confidence > 0.85 && type === 'personal' ? "border-l-ts-purple-500" : ""
    )}>
      <CardContent className="p-4">
        <div className="flex justify-between items-start mb-2">
          <Badge variant="outline" className={cn("font-medium", typeColors[type])}>
            {type.charAt(0).toUpperCase() + type.slice(1)}
          </Badge>
          <span className="text-xs text-muted-foreground">{formattedDate}</span>
        </div>
        
        <div className="space-y-2 mt-3">
          <div className="flex items-start">
            <div className="text-lg font-mono bg-muted p-1 px-2 rounded w-full">
              {maskValue(value, type)}
            </div>
          </div>
          
          <div className="flex justify-between items-center">
            <span className="text-xs text-muted-foreground">Source: {source}</span>
            <ConfidenceBar confidence={confidence} type={type} />
          </div>
        </div>
      </CardContent>
      
      <CardFooter className="px-4 py-3 border-t bg-muted/50 flex justify-end gap-2">
        <Button
          variant="ghost" 
          size="sm"
          onClick={() => onIgnore?.(id)}
        >
          Ignore
        </Button>
        <Button 
          size="sm"
          className={cn(
            type === 'financial' ? "bg-ts-pink-500 hover:bg-ts-pink-600" : 
            "bg-ts-purple-500 hover:bg-ts-purple-600"
          )}
          onClick={() => onEncrypt?.(id)}
        >
          Encrypt
        </Button>
      </CardFooter>
    </Card>
  );
};

export default DetectionItem;
