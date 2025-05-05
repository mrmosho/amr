
import React, { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Search } from "lucide-react";
import DetectionItem, { Detection } from "@/components/Monitoring/DetectionItem";
import SystemTray from "@/components/UI/SystemTray";
import { useToast } from "@/hooks/use-toast";

// Mock data for demonstration
const mockDetections: Detection[] = [
  {
    id: "1",
    timestamp: new Date(2025, 4, 4, 14, 32),
    value: "4532015112830366",
    type: "financial",
    source: "example.docx",
    confidence: 0.92
  },
  {
    id: "2",
    timestamp: new Date(2025, 4, 4, 13, 15),
    value: "johndoe@example.com",
    type: "personal",
    source: "contacts.xlsx",
    confidence: 0.86
  },
  {
    id: "3",
    timestamp: new Date(2025, 4, 4, 10, 45),
    value: "555-123-4567",
    type: "personal",
    source: "customer_data.csv",
    confidence: 0.78
  },
  {
    id: "4",
    timestamp: new Date(2025, 4, 3, 16, 20),
    value: "475019948",
    type: "financial",
    source: "invoice.pdf",
    confidence: 0.95
  },
  {
    id: "5",
    timestamp: new Date(2025, 4, 3, 14, 10),
    value: "123 Main St, Anytown, USA",
    type: "personal",
    source: "shipping_info.doc",
    confidence: 0.82
  },
  {
    id: "6",
    timestamp: new Date(2025, 4, 2, 9, 33),
    value: "1234-5678-9012-3456",
    type: "financial",
    source: "payment_details.txt",
    confidence: 0.88
  }
];

const MonitoringPanel: React.FC = () => {
  const [detections, setDetections] = useState<Detection[]>(mockDetections);
  const [searchTerm, setSearchTerm] = useState("");
  const { toast } = useToast();

  const handleEncrypt = (id: string) => {
    // In a real app, would call an API to encrypt the data
    toast({
      title: "Data encrypted",
      description: "The sensitive data has been successfully encrypted.",
    });
    
    // Remove from the list
    setDetections(detections.filter(d => d.id !== id));
  };

  const handleIgnore = (id: string) => {
    // In a real app, would mark as ignored in the database
    toast({
      title: "Detection ignored",
      description: "This detection will no longer be flagged.",
    });
    
    // Remove from the list
    setDetections(detections.filter(d => d.id !== id));
  };

  const filterDetections = (type?: 'personal' | 'financial') => {
    return detections
      .filter(d => !type || d.type === type)
      .filter(d => 
        searchTerm === "" || 
        d.source.toLowerCase().includes(searchTerm.toLowerCase()) ||
        d.value.toLowerCase().includes(searchTerm.toLowerCase())
      );
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold tracking-tight">Monitoring</h1>
        <Button
          className="bg-ts-purple-500 hover:bg-ts-purple-600"
        >
          Encrypt All
        </Button>
      </div>
      
      <Card>
        <CardHeader>
          <CardTitle>Detection Monitor</CardTitle>
          <CardDescription>
            Review and manage detected sensitive data in your files
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="mb-6">
            <Label htmlFor="search">Search</Label>
            <div className="relative">
              <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                id="search"
                placeholder="Search by source or content..."
                className="pl-8"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>
          
          <Tabs defaultValue="all">
            <TabsList className="grid w-full grid-cols-3 mb-6">
              <TabsTrigger value="all">All ({detections.length})</TabsTrigger>
              <TabsTrigger value="personal">Personal ({filterDetections('personal').length})</TabsTrigger>
              <TabsTrigger value="financial">Financial ({filterDetections('financial').length})</TabsTrigger>
            </TabsList>
            
            <TabsContent value="all" className="space-y-4">
              {filterDetections().length > 0 ? (
                filterDetections().map(detection => (
                  <DetectionItem
                    key={detection.id}
                    detection={detection}
                    onEncrypt={handleEncrypt}
                    onIgnore={handleIgnore}
                  />
                ))
              ) : (
                <div className="text-center py-8">
                  <p className="text-muted-foreground">No detections found</p>
                </div>
              )}
            </TabsContent>
            
            <TabsContent value="personal" className="space-y-4">
              {filterDetections('personal').length > 0 ? (
                filterDetections('personal').map(detection => (
                  <DetectionItem
                    key={detection.id}
                    detection={detection}
                    onEncrypt={handleEncrypt}
                    onIgnore={handleIgnore}
                  />
                ))
              ) : (
                <div className="text-center py-8">
                  <p className="text-muted-foreground">No personal data detections found</p>
                </div>
              )}
            </TabsContent>
            
            <TabsContent value="financial" className="space-y-4">
              {filterDetections('financial').length > 0 ? (
                filterDetections('financial').map(detection => (
                  <DetectionItem
                    key={detection.id}
                    detection={detection}
                    onEncrypt={handleEncrypt}
                    onIgnore={handleIgnore}
                  />
                ))
              ) : (
                <div className="text-center py-8">
                  <p className="text-muted-foreground">No financial data detections found</p>
                </div>
              )}
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
      
      <SystemTray detectionCount={detections.length} />
    </div>
  );
};

export default MonitoringPanel;
