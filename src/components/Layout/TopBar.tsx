
import React from 'react';
import { useTheme } from 'next-themes';
import { Sun, Moon, Bell } from 'lucide-react';
import { Badge } from '@/components/ui/badge';

type SecurityStatus = 'Protected' | 'Warning' | 'At Risk';

const TopBar = () => {
  const { theme, setTheme } = useTheme();
  const [securityStatus, setSecurityStatus] = React.useState<SecurityStatus>('Protected');
  
  const getStatusColor = () => {
    switch (securityStatus) {
      case 'Protected':
        return 'bg-green-500';
      case 'Warning':
        return 'bg-yellow-500';
      case 'At Risk':
        return 'bg-red-500';
      default:
        return 'bg-green-500';
    }
  };

  const toggleTheme = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark');
  };

  return (
    <div className="h-16 border-b flex items-center justify-between px-4 bg-background">
      <div className="flex items-center space-x-4">
        <div className="flex items-center space-x-2">
          <div className={`w-2 h-2 rounded-full ${getStatusColor()}`}></div>
          <Badge variant="outline" className="text-xs font-medium">
            {securityStatus}
          </Badge>
        </div>
      </div>
      
      <div className="flex items-center space-x-2">
        <button 
          onClick={toggleTheme}
          className="p-2 rounded-full hover:bg-muted"
          aria-label="Toggle theme"
        >
          {theme === 'dark' ? <Sun size={18} /> : <Moon size={18} />}
        </button>
        
        <button className="p-2 rounded-full hover:bg-muted relative" aria-label="Notifications">
          <Bell size={18} />
          <span className="absolute top-0 right-0 w-2 h-2 bg-red-500 rounded-full"></span>
        </button>
        
        <div className="w-8 h-8 rounded-full bg-primary text-white flex items-center justify-center text-sm">
          TS
        </div>
      </div>
    </div>
  );
};

export default TopBar;
