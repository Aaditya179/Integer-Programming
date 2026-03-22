class JobSequencingSolver:
    """
    Implements the Greedy algorithm for Job Sequencing with Deadlines.
    
    Jobs are sorted by profit descending, and each job is assigned to the 
    latest possible available slot before its deadline.
    """
    @staticmethod
    def solve(jobs):
        # jobs: list of (id, profit, deadline)
        # Sort jobs by profit in descending order
        n = len(jobs)
        jobs.sort(key=lambda x: x[1], reverse=True)
        
        max_deadline = max(job[2] for job in jobs)
        result = [None] * max_deadline
        total_profit = 0
        sequence = []
        
        for i in range(n):
            # Find a free slot for this job (from its deadline backwards)
            for j in range(min(max_deadline, jobs[i][2]) - 1, -1, -1):
                if result[j] is None:
                    result[j] = jobs[i][0]
                    total_profit += jobs[i][1]
                    break
                    
        sequence = [job_id for job_id in result if job_id is not None]
        return total_profit, sequence
