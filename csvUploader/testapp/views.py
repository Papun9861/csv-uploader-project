from django.shortcuts import render
import io
import csv
from .forms import CSVUploadForm
from .models import Book

# Create your views here.

def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string)
            for row in csv.reader(io_string, delimiter=',', quotechar="|"):
                _, created = Book.objects.update_or_create(
                    title=row[0],
                    author=row[1],
                    publication_date=row[2],
                    price=row[3]
                )
            return render(request, 'success.html')
    else:
        form = CSVUploadForm()
    return render(request, 'testapp/upload.html', {'form': form})
