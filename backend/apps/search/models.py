from django.db import models

class SearchQueryLog(models.Model):
    """
    Optional anonymous search query log for tracking aggregate patterns.
    Never stores personal user identifiers.
    """
    raw_query = models.CharField(max_length=500)
    search_mode = models.CharField(max_length=20, default='fallback')
    results_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.raw_query} ({self.search_mode}) -> {self.results_count} results"
