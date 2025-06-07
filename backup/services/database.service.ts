import { supabase } from '@/lib/supabase';

export type Detection = {
  id: string;
  scan_id: string;
  user_id: string;
  threat_type: 'malware' | 'ransomware' | 'spyware' | 'trojan' | 'other';
  severity: 'low' | 'medium' | 'high' | 'critical';
  file_path: string;
  status: 'detected' | 'quarantined' | 'removed' | 'ignored';
};

export const databaseService = {
  // Scans
  async createScan(userId: string, scanType: 'quick' | 'full' | 'custom') {
    const { data, error } = await supabase
      .from('scans')
      .insert({
        user_id: userId,
        status: 'pending',
        scan_type: scanType
      })
      .select()
      .single();

    if (error) throw error;
    return data;
  },

  // Detections
  async getRecentDetections() {
    const { data, error } = await supabase
      .from('detections')
      .select('*')
      .order('detection_date', { ascending: false })
      .limit(10);

    if (error) throw error;
    return data as Detection[];
  },

  // Stats for Dashboard
  async getDashboardStats(userId: string) {
    const { data: detections, error: detectionsError } = await supabase
      .from('detections')
      .select('*')
      .eq('user_id', userId);

    if (detectionsError) throw detectionsError;

    const { data: latestScan, error: scanError } = await supabase
      .from('scans')
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: false })
      .limit(1)
      .single();

    if (scanError) throw scanError;

    return {
      totalDetections: detections.length,
      lastScanStatus: latestScan.status,
      protectedFiles: latestScan.total_files
    };
  }
};