
import React from 'react';
import { useTheme } from 'next-themes';
import { Sun, Moon, Bell } from 'lucide-react';
import { Badge } from '@/components/ui/badge';

type SecurityStatus = 'Protected' | 'Warning' | 'At Risk';

interface TopBarProps {
  theme?: 'light' | 'dark';
  toggleTheme?: () => void;
}

const TopBar: React.FC<TopBarProps> = ({ theme: propTheme, toggleTheme: propToggleTheme }) => {
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

  const handleToggleTheme = () => {
    if (propToggleTheme) {
      propToggleTheme();
    } else {
      setTheme(theme === 'dark' ? 'light' : 'dark');
    }
  };

  const currentTheme = propTheme || theme;

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
          onClick={handleToggleTheme}
          className="p-2 rounded-full hover:bg-muted"
          aria-label="Toggle theme"
        >
          {currentTheme === 'dark' ? <Sun size={18} /> : <Moon size={18} />}
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
