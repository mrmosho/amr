import React from 'react';
import { Card, CardHeader, CardTitle, CardDescription } from '@/components/UI/card';
import { Users, LayoutDashboard } from 'lucide-react';
import { Button } from '@/components/UI/button';
import { Link } from 'react-router-dom';

interface TeamMember {
  id: number;
  name: string;
  role: string;
}

const AboutUs: React.FC = () => {
  const teamMembers: TeamMember[] = [
    { id: 1, name: 'Omar Husam', role: 'Project Lead' },
    { id: 2, name: 'Amr Mohamed', role: 'Frontend Developer' },
    { id: 3, name: 'Marwan Mohamed', role: 'Security Specialist' },
    { id: 4, name: 'Ahmed Ali', role: 'Backend Developer' },
    { id: 5, name: 'Ibrahim Khaled', role: 'Team Member' },
    { id: 6, name: 'Ziad Abdulrahman', role: 'Team Member' },
  ];

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="flex flex-col items-center justify-center mb-12 text-center">
        <div className="flex items-center gap-2 mb-2">
          <Users className="h-6 w-6 text-primary" />
          <h1 className="text-3xl font-bold">Our Team</h1>
        </div>
        <p className="text-muted-foreground max-w-2xl">
          Meet the dedicated professionals behind TypeSecure — combining expertise in
          cybersecurity, software development, and user experience to create a comprehensive
          sensitive data protection solution.
        </p>
        <Link to="/dashboard" className="mt-4">
          <Button variant="outline" size="sm" className="gap-2">
            <LayoutDashboard className="h-4 w-4" /> Back to Dashboard
          </Button>
        </Link>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {teamMembers.map(member => (
          <Card key={member.id} className="group hover:scale-105 hover:shadow-lg transition-all duration-300">
            <CardHeader className="text-center">
              <CardTitle className="text-lg">{member.name}</CardTitle>
              <CardDescription>{member.role}</CardDescription>
            </CardHeader>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default AboutUs;
